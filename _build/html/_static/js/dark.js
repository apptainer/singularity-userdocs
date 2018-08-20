$(document).ready(function(){
var isdark = false;

  $(".slider.round").click(function(){
          if (!isdark){
            $(".wy-nav-content-wrap").css("background", "#081925");
            $(".wy-nav-content").css("background", "#081925");
            $("body").css("color", "#E0E6ED");
            $("pre").css("color", "#94bfdc");
            $("code").css("background", "#94bfdc").css("border", "solid 1px #a8b2c0");
            $(".highlight").css("background", "#081925");
            $(".highlight pre").css("color", "#fff");
            $("code.literal").css("color", "#000");
            $(".wy-side-nav-search").css("background-color", "#14405c");
            $(".std-ref").css("color", "#5399c7");
            $(".reference.external").css("color", "#d7bce1");
            $(".wy-breadcrumbs li a").css("color", "#d7bce1");
            $("footer a").css("color","#d7bce1");
            isdark = true;
            window.isdark=true;
          }
          else{
            $("footer a").css("color","#9B59B6");
            $(".wy-breadcrumbs li a").css("color", "#9B59B6");
            $(".reference.external").css("color", "#9B59B6");
            $(".std-ref").css("color", "#2980B9");
            $(".wy-nav-content-wrap").css("background", "#fcfcfc");
            $(".wy-nav-content").css("background", "#fcfcfc");
            $("code").css("background", "#fff").css("border", "solid 1px #fff");
            $("body").css("color", "#404040");
            $("code.literal").css("color", "#E74C3C");
            $(".highlight").css("background", "#eeffcc");
            $(".highlight pre").css("color", "#404040");
            $(".wy-side-nav-search").css("background-color", "#2980B9");
            isdark = false;
          }
     });

});
