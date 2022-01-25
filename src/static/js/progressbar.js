// jQuery
class ProgressUI {

    // show the progress bar and progress percentage
    constructor(url, options) {
        this.url = url;
        options = options || {};
        this.mainBarElement = document.getElementById('mainBar')
        this.mainBarTextElement = document.getElementById('mainBarText')
        this.mainBarHeader = document.getElementById('mainBarHeader')
        this.append_func = options.append_func || this.append_func;
    }

    append_func(result) {
        console.log('progress ui end' + result)
    }

    onProgress(percentage, description, header, barElement, barTextElement, barHeader) {
        barElement.style.width = percentage + "%";
        barTextElement.textContent = description;
        barHeader.textContent = header + " " + percentage + "%"
    }
    
    onError(barElement, barTextElement, barHeader) {
        barElement.style.width = '100%'
        barElement.style.backgroundColor = '#dc4f63'
        barTextElement.textContent = "Please read the dianshao_bitbake.log to see the detail"
        barHeader.textContent = "Bitbake Failed"
        $(".subBar").empty();
    }

    success(barElement, barTextElement, barHeader) {
        barElement.style.width = "100%";
        barTextElement.textContent = "";
        barElement.style.backgroundColor = '#4be998';
        barHeader.textContent = "Bitbake Success"
        $(".subBar").empty();
        this.append_func('success');
    }

    onRefreshView(subProgress) {
        $(".subBar").empty();
        for (let i=0; i<subProgress.length; i++) {
            $("#subBarAnchor").append(
                "<div class='subBar'><div id='subBar" + i + "', style='width: " + subProgress[i].percentage + "%; background-color: #f7838d; height: 5px;'></div><p5>"+ subProgress[i].description +"</p5><br></br></div>");
        }
    }

    onData(data) {
        if (data.state == "PROGRESS") {
            this.onRefreshView(data.subProgress)
            this.onProgress(data.percentage, data.description, data.header, this.mainBarElement, this.mainBarTextElement, this.mainBarHeader)
        } else if (data.state == 'SUCCESS') {
            console.log('Task SUCCESS')
            this.success(this.mainBarElement, this.mainBarTextElement, this.mainBarHeader)
        } else if (data.state == 'FAILURE') {
            console.log('Task Failure')
            this.onError(this.mainBarElement, this.mainBarTextElement, this.mainBarHeader)
        }
    }

    async getData() {
        let response;
        let data;
        try {
            response = await fetch(this.url);
        } catch (networkError) {
            console.log('network error');
            throw networkError;
        }

        if (response.status === 200) {
            try {
                data = await response.json();
            } catch (parsingError) {
                console.log('parsing error');
                throw parsingError;
            }
            
            this.onData(data)

            if (data.completed != true) {
                setTimeout(this.getData.bind(this), 100);
            }
        }
    }

    static initProgressBar(url, options) {
        console.log('start progress bar');
        const bar = new this(url, options);
        bar.getData();
    }
}