 (function ($) {
    // initialize the parameter
    var mySelect=function(ele,options){
        this.ele=ele;
        this.defaults={
            mult:false
        };
        this.options=$.extend({},this.defaults,options);
        this.result=[];
    };
    mySelect.prototype={
        init:function(){// initialize the function
            this.pubFunction();
            this.initOption();
            this.closeSelectEvent();
            this.addEvent();
        },
        closeSelectEvent:function(){
            var that=this;
            this.ele.find(".inputWrap").on("click",function(event){
                event.stopPropagation();
                if(that.ele.find(".inputWrap>i").hasClass("fa-angle-down")){
                    that.ele.find(".inputWrap>i").removeClass("fa-angle-down").addClass("fa-angle-up");
                    that.ele.find(".mySelect-option").animate({height:"400px",opacity:"1"},"fast","swing")
                }else{
                    that.ele.find(".inputWrap>i").removeClass("fa-angle-up").addClass("fa-angle-down");
                    that.ele.find(".mySelect-option").animate({height:"0",opacity:"0"},"fast","swing")
                }
            });
            $("html").on("click",function(){
                that.ele.find(".inputWrap>i").removeClass("fa-angle-up").addClass("fa-angle-down");
                that.ele.find(".mySelect-option").animate({height:"0",opacity:"0"},"fast","swing")
            })
        },
        pubFunction:function(){
            Array.prototype.contains = function(obj) {
                var i = this.length;
                while (i--) {
                    if (this[i] === obj) {
                        return i;  // index
                    }
                }
                return false;
            }
        },
        initOption: function () {
            // initialize the input box and option
            this.ele.append('<div class="inputWrap"><ul></ul><i class="fa fa-angle-down"></i></div>');
            this.ele.append('<div class="mySelect-option"></div>');
            for(var i= 0;i<this.options.option.length;i++){
                this.ele.find(".mySelect-option").append('<div data-value="'+this.options.option[i].value+'"><span>'+this.options.option[i].label+'</span><i class="fa fa-check"></i></div>')
            }
        },
        addEvent:function(){
            var that=this;
            this.ele.find(".mySelect-option").find("div").on("click", function (event) {
                event.stopPropagation();
                if(that.options.mult){
                    if($(this).hasClass("selected")){
                        $(this).removeClass("selected");
                        that.result.splice(that.result.contains($(this).attr("data-value")),1)
                    }else{
                        $(this).addClass("selected");
                        that.result.push($(this).attr("data-value"))
                    }
                    that.refreshInput();
                }else{
                    if($(this).hasClass("selected")){
                        $(this).removeClass("selected");
                        that.result='';
                    }else{
                        that.ele.find(".mySelect-option").find("div").removeClass("selected");
                        $(this).addClass("selected");
                        that.result=$(this).attr("data-value");
                        that.ele.find(".inputWrap>i").removeClass("fa-angle-up").addClass("fa-angle-down");
                        that.ele.find(".mySelect-option").animate({height:"0",opacity:"0"},"fast","swing")
                    }
                    that.refreshInput($(this).find("span").text());
                }
                that.options.onChange(that.result)
            });
        },
        inputResultRemoveEvent:function(){
            var that=this;
            this.ele.find(".inputWrap ul li i").on("click",function(event){
                event.stopPropagation();
                that.result.splice(that.result.contains($(this).attr("data-value")),1);
                that.refreshInput();
                that.removeOptionStyle($(this).attr("data-value"));
                that.options.onChange(that.result);
            })
        },
        removeOptionStyle:function(val){
            this.ele.find(".mySelect-option").find("div").each(function(){
                if($(this).attr("data-value")==val){
                    $(this).removeClass("selected")
                }
            })
        },
        refreshInput:function(label){
            this.ele.find(".inputWrap ul").empty();
            if(this.options.mult){
                for(var i=0;i<this.options.option.length;i++){
                    for(var j=0;j<this.result.length;j++){
                        if(this.result[j]==this.options.option[i].value){
                            this.ele.find(".inputWrap ul").append('<li><span>'+this.options.option[i].label+'</span>&nbsp;&nbsp;<i data-value="'+this.options.option[i].value+'" class="fa fa-close"></i></li>')
                        }
                    }
                }
            }else{
                if(this.result==''){
                    this.ele.find(".inputWrap ul").empty()
                }else{
                    this.ele.find(".inputWrap ul").append('<li><span>'+label+'</span>&nbsp;&nbsp;</li>')
                }

            }
            this.inputResultRemoveEvent();
        },
        setResult:function(res){
            this.result=res;
            if(this.options.mult){
                if(res instanceof Array){
                    this.refreshInput();
                    this.ele.find(".mySelect-option").find("div").each(function(){
                        for(var i=0;i<res.length;i++){
                            if($(this).attr("data-value")==res[i]){
                                $(this).addClass("selected")
                            }
                        }

                    })
                }else{
                    alert("参数必须是数组")
                }

            }else{
                for(var i=0;i<this.options.option.length;i++){
                    if(this.options.option[i].value==res){
                        this.refreshInput(this.options.option[i].label)
                    }
                }
                this.ele.find(".mySelect-option").find("div").each(function(){
                        if($(this).attr("data-value")==res){
                            $(this).addClass("selected")
                        }
                })
            }

        },
        getResult:function(){
            return this.result;
        }
    };
    $.fn.mySelect=function(options){
        var select=new mySelect(this,options);
        select.init();
        return select;
    };
})(jQuery);