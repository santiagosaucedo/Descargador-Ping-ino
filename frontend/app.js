const canvas = document.getElementById('appCanvas');
const ctx = canvas.getContext('2d');
const urlInput = document.getElementById('urlInput');
const fileInput = document.getElementById('fileInput');

const COLORES = {
    fondoPrincipal: '#1A1A1A',
    sidebar: '#242424',
    botonSidebar: '#3A3A3A',
    botonActivo: '#505050',
    textoPerla: '#EAEAEA',
    bordeContenedor: '#2A2A2A',
    inputFondo: '#111111',
    botonError: '#992222',
    botonPresionado: '#282828',
    inputActivo: '#444444'
};

const ANCHO_SIDEBAR = 130; 

// --- ESTADO DE LA APLICACIÓN ---
let vistaActual = 'DES'; 
let botonProcesarEstado = 'reposo'; 

let archivoLocalCargado = false; 
let nombreArchivoSeleccionado = ""; 

let inputSeleccionado = false;
urlInput.addEventListener('focus', () => { inputSeleccionado = true; renderizarInterfaz(); });
urlInput.addEventListener('blur', () => { inputSeleccionado = false; renderizarInterfaz(); });

urlInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault(); 
        if (vistaActual === 'DES') {
            ejecutarAccionDescarga();
        }
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        archivoLocalCargado = true;
        nombreArchivoSeleccionado = e.target.files[0].name; 
        botonProcesarEstado = 'reposo'; 
        renderizarInterfaz(); 
    }
});

function dibujarRectRedondeado(x, y, ancho, alto, radio, color, strokeColor = null) {
    ctx.beginPath();
    ctx.moveTo(x + radio, y);
    ctx.lineTo(x + ancho - radio, y);
    ctx.quadraticCurveTo(x + ancho, y, x + ancho, y + radio);
    ctx.lineTo(x + ancho, y + alto - radio);
    ctx.quadraticCurveTo(x + ancho, y + alto, x + ancho - radio, y + alto);
    ctx.lineTo(x + radio, y + alto);
    ctx.quadraticCurveTo(x, y + alto, x, y + alto - radio);
    ctx.lineTo(x, y + radio);
    ctx.quadraticCurveTo(x, y, x + radio, y);
    ctx.closePath();
    ctx.fillStyle = color;
    ctx.fill();
    if (strokeColor) {
        ctx.strokeStyle = strokeColor;
        ctx.lineWidth = 1.5;
        ctx.stroke();
    }
}

function renderizarInterfaz() {
    ctx.fillStyle = COLORES.fondoPrincipal;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = COLORES.sidebar;
    ctx.fillRect(0, 0, ANCHO_SIDEBAR, canvas.height);
    
    ctx.strokeStyle = '#2D2D2D';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(ANCHO_SIDEBAR, 0);
    ctx.lineTo(ANCHO_SIDEBAR, canvas.height);
    ctx.stroke();

    ctx.font = 'bold 13px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    let colorDes = (vistaActual === 'DES') ? COLORES.botonActivo : COLORES.botonSidebar;
    dibujarRectRedondeado(15, 30, 100, 45, 8, colorDes);
    ctx.fillStyle = COLORES.textoPerla;
    ctx.fillText('Descarga', 65, 52);

    let colorMp3 = (vistaActual === 'MP3') ? COLORES.botonActivo : COLORES.botonSidebar;
    dibujarRectRedondeado(15, 90, 100, 45, 8, colorMp3);
    ctx.fillStyle = COLORES.textoPerla;
    ctx.fillText('MP3', 65, 112);

    if (vistaActual === 'DES') {
        urlInput.style.display = 'block';
        fileInput.style.display = 'none'; 
        renderizarVistaDescarga();
    } else if (vistaActual === 'MP3') {
        urlInput.style.display = 'none';
        
        if (botonProcesarEstado === 'reposo') {
            fileInput.style.display = 'block';
        } else {
            fileInput.style.display = 'none';
        }
        
        renderizarVistaConversion();
    }
}

function renderizarVistaDescarga() {
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    let cajaAncho = 500;
    let cajaAlto = 240;
    let cajaX = ANCHO_SIDEBAR + ((canvas.width - ANCHO_SIDEBAR) - cajaAncho) / 2; 
    let cajaY = 60;

    let colorCajaActual = '#222222';
    let textoCajaActual = 'Descargar Video / Audio';

    if (botonProcesarEstado === 'pulsado') colorCajaActual = COLORES.botonPresionado;
    else if (botonProcesarEstado === 'error') { colorCajaActual = COLORES.botonError; textoCajaActual = 'URL inválida o vacía'; }
    else if (botonProcesarEstado === 'descargando') { colorCajaActual = '#225588'; textoCajaActual = 'Procesando descarga...'; }
    else if (botonProcesarEstado === 'exito') { colorCajaActual = '#226622'; textoCajaActual = 'Descarga Exitosa'; }

    dibujarRectRedondeado(cajaX, cajaY, cajaAncho, cajaAlto, 12, colorCajaActual, COLORES.bordeContenedor);
    ctx.fillStyle = COLORES.textoPerla;
    ctx.font = '22px sans-serif';
    ctx.fillText(textoCajaActual, cajaX + (cajaAncho/2), cajaY + (cajaAlto/2));

    let inputX = cajaX;
    let inputY = 340;
    let inputAncho = cajaAncho;
    let inputAlto = 50;
    let colorBordeInput = inputSeleccionado ? COLORES.inputActivo : '#333333';

    dibujarRectRedondeado(inputX, inputY, inputAncho, inputAlto, 6, COLORES.inputFondo, colorBordeInput);
}

function renderizarVistaConversion() {
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    let zonaAncho = 500;
    let zonaAlto = 240;
    let zonaX = ANCHO_SIDEBAR + ((canvas.width - ANCHO_SIDEBAR) - zonaAncho) / 2;
    let zonaY = 60;

    let fondoZona = archivoLocalCargado ? '#1D2A1D' : '#222222'; 
    dibujarRectRedondeado(zonaX, zonaY, zonaAncho, zonaAlto, 12, fondoZona, COLORES.bordeContenedor);
    
    if (!archivoLocalCargado) {
        ctx.fillStyle = COLORES.textoPerla;
        ctx.font = '40px sans-serif';
        ctx.fillText('🎬', zonaX + (zonaAncho/2), zonaY + (zonaAlto/2) - 30); 

        ctx.font = '20px sans-serif';
        ctx.fillText('Añadir archivo video', zonaX + (zonaAncho/2), zonaY + (zonaAlto/2) + 20);
        
        ctx.fillStyle = '#666666';
        ctx.font = '13px sans-serif';
        ctx.fillText('(Arrastrá el archivo acá o hacé click para buscar)', zonaX + (zonaAncho/2), zonaY + (zonaAlto/2) + 50);
    } else {
        ctx.fillStyle = COLORES.textoPerla;
        ctx.font = '40px sans-serif';
        ctx.fillText('📄', zonaX + (zonaAncho/2), zonaY + (zonaAlto/2) - 30); 

        ctx.font = 'bold 16px sans-serif';
        ctx.fillStyle = '#66BB66'; 
        ctx.fillText('Video listo para procesar', zonaX + (zonaAncho/2), zonaY + (zonaAlto/2) + 15);
        
        ctx.fillStyle = COLORES.textoPerla;
        ctx.font = 'italic 13px monospace';
        
        let nombreCorto = nombreArchivoSeleccionado;
        if (nombreCorto.length > 45) nombreCorto = nombreCorto.substring(0, 42) + "...";
        ctx.fillText(nombreCorto, zonaX + (zonaAncho/2), zonaY + (zonaAlto/2) + 45);
    }

    let btnX = zonaX;
    let btnY = 340;
    let btnAncho = zonaAncho;
    let btnAlto = 50;

    let colorBotonActual = COLORES.botonSidebar;
    let textoBotonActual = 'Descargar y Convertir a MP3';

    if (botonProcesarEstado === 'pulsado') colorBotonActual = COLORES.botonPresionado;
    else if (botonProcesarEstado === 'error') { colorBotonActual = COLORES.botonError; textoBotonActual = 'No se cargo ningun archivo'; }
    else if (botonProcesarEstado === 'procesando') { colorBotonActual = '#226622'; textoBotonActual = 'Convirtiendo a MP3'; }

    dibujarRectRedondeado(btnX, btnY, btnAncho, btnAlto, 8, colorBotonActual, '#444444');
    ctx.fillStyle = COLORES.textoPerla;
    ctx.font = 'bold 15px sans-serif';
    ctx.fillText(textoBotonActual, btnX + (btnAncho/2), btnY + (btnAlto/2));
}

// CONTROLADOR COMPARTIDO DE RESPUESTA DE DESCARGA
function procesarResultadoDescarga(respuesta) {
    if (respuesta.status === "ok") {
        botonProcesarEstado = 'exito'; 
        urlInput.value = ""; 
        renderizarInterfaz();

        setTimeout(() => {
            botonProcesarEstado = 'reposo';
            renderizarInterfaz();
        }, 3000);
    } else {
        botonProcesarEstado = 'error';
        renderizarInterfaz();
        setTimeout(() => { botonProcesarEstado = 'reposo'; renderizarInterfaz(); }, 3000);
    }
}

// CONTROLADOR COMPARTIDO DE RESPUESTA DE CONVERSIÓN
function procesarResultadoConversion(respuesta) {
    if (respuesta.status === "ok") {
        setTimeout(() => {
            botonProcesarEstado = 'reposo';
            archivoLocalCargado = false;
            nombreArchivoSeleccionado = "";
            fileInput.value = ""; 
            renderizarInterfaz();
        }, 2500);
    } else {
        botonProcesarEstado = 'error';
        renderizarInterfaz();
        setTimeout(() => { botonProcesarEstado = 'reposo'; renderizarInterfaz(); }, 3000);
    }
}

function ejecutarAccionDescarga() {
    if (botonProcesarEstado !== 'reposo') return;

    let urlTexto = urlInput.value;
    let urlValida = urlTexto.includes("youtube.com") || urlTexto.includes("youtu.be");

    if (!urlValida || urlTexto.trim() === "") {
        botonProcesarEstado = 'error';
        renderizarInterfaz();
        setTimeout(() => { botonProcesarEstado = 'reposo'; renderizarInterfaz(); }, 2000);
    } else {
        botonProcesarEstado = 'descargando';
        renderizarInterfaz();

        // 🐧 Validamos si Eel está activo REALMENTE (comprobando sus funciones expuestas de PC)
        if (window.eel && typeof window.eel.backend_descargar_video === 'function') {
            eel.backend_descargar_video(urlTexto)(procesarResultadoDescarga);
        } else {
            // Android entra directo por acá usando la API REST local
            fetch('/api/descargar_video', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: urlTexto })
            })
            .then(res => res.json())
            .then(procesarResultadoDescarga)
            .catch(() => {
                console.error("Error en fetch de descarga");
                procesarResultadoDescarga({ status: "error" });
            });
        }
    }
}

function ejecutarAccionConversionLocal() {
    if (botonProcesarEstado !== 'reposo') return;

    if (!archivoLocalCargado || fileInput.files.length === 0) {
        botonProcesarEstado = 'error';
        renderizarInterfaz();
        setTimeout(() => { botonProcesarEstado = 'reposo'; renderizarInterfaz(); }, 2000);
        return;
    }

    botonProcesarEstado = 'procesando';
    renderizarInterfaz();

    const archivoReal = fileInput.files[0];
    const lector = new FileReader();
    
    lector.onload = function(evento) {
        const arrayBuffer = evento.target.result;
        const bytes = new Uint8Array(arrayBuffer);
        
        let hexString = "";
        for (let i = 0; i < bytes.length; i++) {
            hexString += bytes[i].toString(16).padStart(2, '0');
        }

        // Validamos puente real de escritorio
        if (window.eel && typeof window.eel.backend_convertir_bytes_a_mp3 === 'function') {
            eel.backend_convertir_bytes_a_mp3(archivoReal.name, hexString)(procesarResultadoConversion);
        } else {
            fetch('/api/convertir_bytes', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nombre: archivoReal.name, hex: hexString })
            })
            .then(res => res.json())
            .then(procesarResultadoConversion)
            .catch(() => procesarResultadoConversion({ status: "error" }));
        }
    };

    lector.readAsArrayBuffer(archivoReal);
}

// --- INTERACCIÓN DEL MOUSE ---
canvas.addEventListener('click', function(event) {
    const rect = canvas.getBoundingClientRect();
    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;

    if (mouseX >= 15 && mouseX <= 115 && mouseY >= 30 && mouseY <= 75) {
        if (vistaActual !== 'DES') {
            vistaActual = 'DES';
            botonProcesarEstado = 'reposo'; 
            renderizarInterfaz();
        }
        return;
    }

    if (mouseX >= 15 && mouseX <= 115 && mouseY >= 90 && mouseY <= 135) {
        if (vistaActual !== 'MP3') {
            vistaActual = 'MP3';
            botonProcesarEstado = 'reposo';
            renderizarInterfaz();
        }
        return;
    }

    let cajaAncho = 500;
    let cajaX = ANCHO_SIDEBAR + ((canvas.width - ANCHO_SIDEBAR) - cajaAncho) / 2;

    if (vistaActual === 'DES') {
        if (mouseX >= cajaX && mouseX <= (cajaX + cajaAncho) && mouseY >= 60 && mouseY <= 300) {
            ejecutarAccionDescarga();
        }
    } 
    else if (vistaActual === 'MP3') {
        if (mouseX >= cajaX && mouseX <= (cajaX + cajaAncho) && mouseY >= 340 && mouseY <= 390) {
            ejecutarAccionConversionLocal();
        }
    }
});

renderizarInterfaz();