//#region class

class RGBColor
{
    constructor(R, G, B) {
        this.R = parseInt(R);
        this.G = parseInt(G);
        this.B = parseInt(B);
    }

    ColorToCssColor()
    {
        return "rgb("+this.R+","+this.G+","+this.B+")";
    }
}

//#endregion

document.write(1 + 1);

var test_slider = document.getElementById("testSlider");
var test_slider_output = document.getElementById("sliderValue")

var main_color = new RGBColor(223, 249, 255);
var main_color2 = new RGBColor(223, 230, 255); 

test_slider.oninput = function()
{
    test_slider_output.innerHTML = this.value;
    changeBackGroundColor(this.value / (this.max - this.min));
}

//#region color

function RgbColor(R, G, B)
{
    this.R = parseInt(R);
    this.G = parseInt(G);
    this.B = parseInt(B);
}

function LerpColor(Color1, Color2, alpha)
{
    var R = Color1.R + (Color2.R - Color1.R) * parseFloat(alpha);
    var G = Color1.G + (Color2.G - Color1.G) * parseFloat(alpha);
    var B = Color1.B + (Color2.B - Color1.B) * parseFloat(alpha);
    return new RGBColor(R,G,B);
}

function changeBackGroundColor(alpha)
{
    document.body.style.backgroundColor 
    = LerpColor(main_color, main_color2, alpha).ColorToCssColor();
    // document.write(LerpColor(main_color, main_color2, alpha).ColorToCssColor());
    document.getElementById("result").innerText
    = document.body.style.backgroundColor ;
}

//#endregion