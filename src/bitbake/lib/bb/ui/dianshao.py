import sys
import os
import socket
import json

try:
    import bb
    import bb.event
    import bb.build
    import bb.command
    import bb.cooker
    import bb.exceptions
    import bb.runqueue
    import bb.msg
    from bb.ui import uihelper
except RuntimeError as exc:
    sys.exit(str(exc))

featureSet = [bb.cooker.CookerFeatures.SEND_SANITYEVENTS]

import logging
logger = logging.getLogger("DianshaoLogger")
interactive = sys.stdout.isatty()

def pluralise(singular, plural, qty):
    if(qty == 1):
        return singular % qty
    else:
        return plural % qty

_evt_list = [ 
    "bb.runqueue.runQueueExitWait",
    "bb.event.LogExecTTY",
    "logging.LogRecord",
    "bb.build.TaskFailed",
    "bb.build.TaskBase",
    "bb.event.ParseStarted",
    "bb.event.ParseProgress",
    "bb.event.ParseCompleted",
    "bb.event.CacheLoadStarted",
    "bb.event.CacheLoadProgress",
    "bb.event.CacheLoadCompleted",
    "bb.command.CommandFailed",
    "bb.command.CommandExit",
    "bb.command.CommandCompleted",
    "bb.cooker.CookerExit",
    "bb.event.MultipleProviders",
    "bb.event.NoProvider",
    "bb.runqueue.sceneQueueTaskStarted",
    "bb.runqueue.runQueueTaskStarted",
    "bb.runqueue.runQueueTaskFailed",
    "bb.runqueue.sceneQueueTaskFailed",
    "bb.event.BuildBase",
    "bb.build.TaskStarted",
    "bb.build.TaskSucceeded",
    "bb.build.TaskFailedSilent",
    "bb.build.TaskProgress",
    "bb.event.ProcessStarted",
    "bb.event.ProcessProgress",
    "bb.event.ProcessFinished"
    ] 

def main(server, eventHandler, params):
    print("welcom to dianshao yocto ui\n")
    dianshao_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dianshao_server_addr = ('127.0.0.1', 6688)
    dianshao_client.settimeout(0.1)
    dianshao_client.sendto(json.dumps({'event_type': 'dianshao_ui_start'}).encode('ascii'), dianshao_server_addr)

    helper = uihelper.BBUIHelper()

    params.updateToServer(server, os.environ.copy())
    params.updateFromServer(server)

    # TODO: 整理 log 功能，形成日志文档
    console = logging.StreamHandler(sys.stdout)
    format_str = "%(levelname)s: %(message)s"
    formatter = bb.msg.BBLogFormatter(format_str)
    bb.msg.addDefaultlogFilter(console)
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.setLevel(logging.INFO)
    llevel, debug_domains = bb.msg.constructLogOptions()
    result, error = server.runCommand(["setEventMask", server.getEventHandle(), llevel, debug_domains, _evt_list])
    if not result or error:
        logger.error("can't set event mask: %s", error)
        return 1

    cmdline = params.parseActions()
    if not cmdline:
        print("Nothing to do.  Use 'bitbake world' to build everything, or run 'bitbake --help' for usage information.")
        return 1

    ret, error = server.runCommand(cmdline['action'])        
    if error:
        logger.error("Command '%s' failed: %s" % (cmdline, error))
        return 1
    elif not ret:
        logger.error("Command '%s' failed: returned %s" % (cmdline, ret))
        return 1
    
    main.shutdown = 0
    return_value = 0
    errors = 0
    warnings = 0
    taskfailures = []
    
    while True:
        try:
            event = eventHandler.waitEvent(0.5)

            if event is None:
                if main.shutdown > 1:
                    break
                
                activeTasks = helper.running_tasks
                runningpids = helper.running_pids

                tasks = []
                for t in runningpids:
                    progress = activeTasks[t].get("progress", None)
                    if progress is not None:
                        rate = activeTasks[t].get("rate", None)
                        title = activeTasks[t]['title']
                        task = {'progress': progress, 'rate': rate, 'title': title}
                        tasks.append(task)

                if len(tasks) > 0:
                    dianshao_client.sendto(json.dumps({'event_type': 'TaskList', 'tasks': tasks}).encode('ascii'), dianshao_server_addr)
                
                event = eventHandler.waitEvent(0.5)
                if event is None:
                    dianshao_client.sendto(json.dumps({'event_type': 'Ping'}).encode('ascii'), dianshao_server_addr)
                    try:
                        msg, addr = dianshao_client.recvfrom(1024)
                        server_command = json.loads(msg.decode('ascii'))
                        if server_command['event_type'] == 'PONG':
                            if server_command['command'] == 'shutdown':
                                main.shutdown = 2

                    except socket.timeout:
                        pass

                    continue

            helper.eventHandler(event)
            # TODO: 将有效信息通过JSON传递
            if isinstance(event, bb.runqueue.runQueueExitWait):
                if not main.shutdown:
                    main.shutdown = 1
                continue

            if isinstance(event, bb.event.LogExecTTY):
                dianshao_client.sendto(json.dumps({'event_type': 'LogExecTTY',
                                                'msg': event.msg}).encode('ascii'), dianshao_server_addr)
                continue

            if isinstance(event, logging.LogRecord):
                if event.levelno >= logging.ERROR:
                    print('lxy')
                    errors = errors + 1
                    return_value = 1
                elif event.levelno == logging.WARNING:
                    warnings = warnings + 1

                """
                dianshao_client.sendto(json.dumps({'event_type': 'LogRecord',
                                                'msg': event.msg}).encode('ascii'), dianshao_server_addr)
                """

                logging.getLogger(event.name).handle(event)
                continue

            if isinstance(event, bb.event.ParseStarted):
                dianshao_client.sendto(json.dumps({'event_type': 'ParseStarted',
                                                'total': event.total}).encode('ascii'), dianshao_server_addr)
                continue

            if isinstance(event, bb.event.ParseCompleted):
                dianshao_client.sendto(json.dumps({'event_type': 'ParseCompleted',
                                                'total': event.total, 'cached': event.cached,
                                                'parsed': event.parsed, 'virtuals': event.virtuals,
                                                'skipped': event.skipped, 'masked': event.masked,
                                                'errors': event.errors}).encode('ascii'), dianshao_server_addr)
                continue

            if isinstance(event, bb.build.TaskFailedSilent):
                logger.warning("Logfile for failed setscene task is %s" % event.logfile)
                continue

            if isinstance(event, bb.build.TaskBase):
                logger.info(event._message)
                dianshao_client.sendto(json.dumps({'event_type': 'TaskBase',
                                                'message': event._message}).encode('ascii'), dianshao_server_addr)
                continue

            if isinstance(event, bb.build.TaskFailed):
                dianshao_client.sendto(json.dumps({'event_type': 'TaskFailed',
                                                'name': event.taskname}).encode('ascii'), dianshao_server_addr)
                return_value = 1
                continue

            if isinstance(event, bb.event.ParseProgress):
                dianshao_client.sendto(json.dumps({'event_type': 'ParseProgress',
                                                'current': event.current, 
                                                'total': event.total}).encode('ascii'), dianshao_server_addr)
                continue

            if isinstance(event, bb.event.CacheLoadStarted):
                dianshao_client.sendto(json.dumps({'event_type': 'CacheLoadStarted', 
                                                'total': event.total}).encode('ascii'), dianshao_server_addr)
                continue

            if isinstance(event, bb.event.CacheLoadProgress):
                dianshao_client.sendto(json.dumps({'event_type': 'CacheLoadProgress', 
                                                'total': event.total, 'current': event.current}).encode('ascii'), dianshao_server_addr)
                continue

            if isinstance(event, bb.event.CacheLoadCompleted):
                dianshao_client.sendto(json.dumps({'event_type': 'CacheLoadCompleted',
                                                'num_entries': event.num_entries}).encode('ascii'), dianshao_server_addr)
                continue

            if isinstance(event, bb.command.CommandFailed):
                """
                dianshao_client.sendto(json.dumps({'event_type': 'CommandFailed'
                                                }).encode('ascii'), dianshao_server_addr)
                """
                return_value = event.exitcode
                if event.error:
                    errors = errors + 1
                    logger.error(str(event))
                main.shutdown = 2
                continue

            if isinstance(event, bb.command.CommandExit):
                if not return_value:
                    return_value = event.exitcode
                """
                dianshao_client.sendto(json.dumps({'event_type': 'CommandExit'
                                            }).encode('ascii'), dianshao_server_addr)  
                """
                main.shutdown = 2
                continue

            if isinstance(event, (bb.command.CommandCompleted, bb.cooker.CookerExit)):
                """
                dianshao_client.sendto(json.dumps({'event_type': 'CommandCompleted'
                                            }).encode('ascii'), dianshao_server_addr)                
                """
                main.shutdown = 2
                continue

            if isinstance(event, bb.event.MultipleProviders):
                logger.info(str(event))
                continue

            if isinstance(event, bb.event.NoProvider):
                logger.warning(str(event))
                continue

            if isinstance(event, bb.runqueue.sceneQueueTaskStarted):
                dianshao_client.sendto(json.dumps({'event_type': 'sceneQueueTaskStarted',
                                                'current': event.stats.setscene_covered + event.stats.setscene_active + event.stats.setscene_notcovered + 1,
                                                'total': event.stats.setscene_total,
                                                'taskstring': event.taskstring}).encode('ascii'), dianshao_server_addr)
                continue

            if isinstance(event, bb.runqueue.runQueueTaskStarted):
                dianshao_client.sendto(json.dumps({'event_type': 'runQueueTaskStarted',
                                                'current': event.stats.completed + event.stats.active + event.stats.failed + 1,
                                                'total': event.stats.total,
                                                'taskstring': event.taskstring}).encode('ascii'), dianshao_server_addr)
                continue            

            if isinstance(event, bb.runqueue.runQueueTaskFailed):
                return_value = 1
                logger.error(str(event))
                taskfailures.append(event.taskstring)
                dianshao_client.sendto(json.dumps({'event_type': 'runQueueTaskFailed',
                                                'taskstring': event.taskstring}).encode('ascii'), dianshao_server_addr)
                continue

            if isinstance(event, bb.runqueue.sceneQueueTaskFailed):
                logger.warning(str(event))
                dianshao_client.sendto(json.dumps({'event_type': 'sceneQueueTaskFailed',
                                'taskstring': event.taskstring}).encode('ascii'), dianshao_server_addr)
                continue

            if isinstance(event, bb.event.DepTreeGenerated):
                continue

            if isinstance(event, bb.event.ProcessStarted):
                dianshao_client.sendto(json.dumps({'event_type': 'ProcessStarted',
                                                'processname': event.processname,
                                                'total': event.total}).encode('ascii'), dianshao_server_addr)
                continue

            if isinstance(event, bb.event.ProcessProgress):
                dianshao_client.sendto(json.dumps({'event_type': 'ProcessProgress',
                                                'processname': event.processname,
                                                'progress': event.progress}).encode('ascii'), dianshao_server_addr)
                continue

            if isinstance(event, bb.event.ProcessFinished):
                dianshao_client.sendto(json.dumps({'event_type': 'ProcessFinished',
                                                'processname': event.processname,}).encode('ascii'), dianshao_server_addr)
                continue

            # ignore
            if isinstance(event, (bb.event.BuildBase,
                                  bb.event.MetadataEvent,
                                  bb.event.ConfigParsed,
                                  bb.event.MultiConfigParsed,
                                  bb.event.RecipeParsed,
                                  bb.event.RecipePreFinalise,
                                  bb.runqueue.runQueueEvent,
                                  bb.event.OperationStarted,
                                  bb.event.OperationCompleted,
                                  bb.event.OperationProgress,
                                  bb.event.DiskFull,
                                  bb.event.HeartbeatEvent,
                                  bb.build.TaskProgress)):
                continue
            
            logger.error("Unknown event: %s", event)

        except EnvironmentError as ioerror:
            # ignore interrupted io
            if ioerror.args[0] == 4:
                continue
            sys.stderr.write(str(ioerror))
            if not params.observe_only:
                _, error = server.runCommand(["stateForceShutdown"])
            main.shutdown = 2
        except Exception as e:
            import traceback
            sys.stderr.write(traceback.format_exc())
            if not params.observe_only:
                _, error = server.runCommand(["stateForceShutdown"])
            main.shutdown = 2
            return_value = 1 

    summary = ""

    if taskfailures:
        summary += pluralise("\nSummary: %s task failed:",
                                "\nSummary: %s tasks failed:", len(taskfailures))
        for failure in taskfailures:
            summary += "\n  %s" % failure
    if warnings:
        summary += pluralise("\nSummary: There was %s WARNING message shown.",
                                "\nSummary: There were %s WARNING messages shown.", warnings)
    if return_value and errors:
        summary += pluralise("\nSummary: There was %s ERROR message shown, returning a non-zero exit code.",
                                "\nSummary: There were %s ERROR messages shown, returning a non-zero exit code.", errors)


    dianshao_client.sendto(json.dumps({'event_type': 'End', 'total_error': errors,
                                    'total_warning': warnings, 'total_task_failures': len(taskfailures)}).encode('ascii'), dianshao_server_addr)
    """
    dianshao_client.sendto(json.dumps({'event_type': 'Summary',
                                'summary': summary, 'total_error': errors, 'total_warning': warnings, 
                                'total_task_failures': len(taskfailures)}).encode('ascii'), dianshao_server_addr)
    """
    logging.shutdown()
    print('dianshao out')
    dianshao_client.close()
    return return_value