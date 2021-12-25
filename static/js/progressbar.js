// jQuery
class ProgressUI {

    // show the progress bar and progress percentage
    constructor(url, options) {
        this.url = url;
        options = options || {};
        this.mainBarElement = document.getElementById('mainBar')
        this.mainBarTextElement = document.getElementById('mainBarText')
        this.append_func = options.append_func || this.append_func;
    }

    append_func(result) {
        console.log('progress ui end' + result)
    }

    onProgress(percentage, description, barElement, barTextElement) {
        barElement.style.width = percentage + "%";
        barTextElement.textContent = description + " " + percentage + "%";
    }

    success(percentage, description, barElement, barTextElement) {
        barElement.style.width = percentage + "%";
        barTextElement.textContent = description + " " + percentage + "%";
        barElement.style.backgroundColor = '#4be998';
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
            this.onProgress(data.percentage, data.description, this.mainBarElement, this.mainBarTextElement)
        } else if (data.state == 'SUCCESS') {
            this.success(100, "success", this.mainBarElement, this.mainBarTextElement)
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