const canvasId = "circules_canvas";

function setSizeCanvas(id, h=480, w=640) {
    const params = new URLSearchParams(window.location.search);

    const height = parseFloat(params.get("h"));
    const width = parseFloat(params.get("w"));

    const canvas = document.getElementById(id);
    if (width > 0) {
        canvas.setAttribute("width", width);
        w = width;
        if (!height) {
            canvas.setAttribute("height", width);
            h = width;
        }
    }
    if (height > 0) {
        canvas.setAttribute("height", height);
        h = height;
        if (!width) {
            canvas.setAttribute("width", height);
            w = height;
        }
    }

    return [h, w];
}

function drawCanvasElements(id, ncircles) {

    const canvas = document.getElementById(id);

    let ctx = canvas.getContext("2d");

    const w = canvas.width;
    const h = canvas.height;
    const n = ncircles;

    const ratio = w / h;
    const cols = Math.sqrt(n * ratio);
    const rows = Math.ceil(n / cols);

    // Melhor opção ocupando toda altura
    {
        let _rows = Math.ceil(rows);
        let _cols = Math.ceil(n / _rows);

        if (_rows * ratio < _cols) {
            const rowsRatio = _cols / (_rows * ratio);
            _rows = Math.ceil(_rows * rowsRatio);
            _cols = Math.ceil(n / _rows);
        }

        var fullHeightSide = h / _rows;
    }

    // Melhor opção ocupando toda largura
    {
        let _cols = Math.ceil(cols);
        let _rows = Math.ceil(n / _cols);

        if (_rows * ratio > _cols) {
            const colsRatio = (_rows * ratio) / _cols;
            _cols = Math.ceil(_cols * colsRatio);
            _rows = Math.ceil(n / _cols);
        }

        var fullWidthSide = w / _cols;
    }

    // Finalmente 
    let squareSide = Math.max(fullHeightSide, fullWidthSide);

    $("#n_circles").html(`${ncircles}`);
    $("#row_cols").html(`(${Math.round(cols)}x${Math.round(rows)})`);

    // My solution is identical to the code below...
    let perRow = Math.floor(canvas.width / squareSide)
    let circleRadius = squareSide / 4;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "black";
    ctx.strokeStyle = "gray";
    for (let i = 0; i < ncircles; i++) {
        let row = Math.floor(i / perRow);
        let col = i % perRow;
        let x = circleRadius * 2 + circleRadius * 4 * col;
        let y = circleRadius * 2 + circleRadius * 4 * row;
        ctx.beginPath();
        ctx.arc(x, y, circleRadius, 0, Math.PI * 2)
        ctx.fill()
        ctx.beginPath();
        ctx.moveTo(x - squareSide / 2, y - squareSide / 2);
        ctx.lineTo(x - squareSide / 2, y + squareSide / 2);
        ctx.lineTo(x + squareSide / 2, y + squareSide / 2);
        ctx.lineTo(x + squareSide / 2, y - squareSide / 2);
        ctx.closePath();
        ctx.stroke()
    }

    return squareSide;
}

function setValorSlider(v) {
    const slider = document.getElementById("n");

    slider.value = v;
}

function slideHandler() {
    let slider = document.getElementById("n");
    console.log("valor: ", setCookie);
    
    setCookie("valor", slider.value, 1);
    console.log("cookie  ", getCookie("valor"));

    $("#range").html(`${slider.value}`);
    drawCanvasElements(canvasId, parseInt(slider.value));
}

function main() {
    const [h, w] = setSizeCanvas(canvasId);
    $("#canvas_titulo1").html(`Canvas: (${w}x${h})`);
    $("#canvas_titulo2").html(`Aspect ratio: ${(w/h).toFixed(2)}`);

    const sliderValue = getCookie("valor") ? getCookie("valor") : "25";

    setValorSlider(sliderValue);
    drawCanvasElements(canvasId, sliderValue)
    dragAndSave("#" + canvasId);
}

main();