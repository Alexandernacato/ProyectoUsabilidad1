document.addEventListener("DOMContentLoaded", () => {

    const urlParams = new URLSearchParams(window.location.search);
    const role = urlParams.get("role");
        // Seleccionar las secciones de la barra lateral y contenido
        const usuariosLink = document.querySelector('a[href="./Usuario.html"]');
        const categoriasLink = document.querySelector('a[href="./categoria.html"]');
        const productosLink = document.querySelector('a[href="./productos.html"]');
        const ventasLink = document.querySelector('a[href="./venta.html"]');
    
        const usuariosCard = document.getElementById("usuarios-count").closest(".col-md-3");
        const categoriasCard = document.getElementById("categorias-count").closest(".col-md-3");
        const productosCard = document.getElementById("productos-count").closest(".col-md-3");
        const ventasCard = document.getElementById("ventas-count").closest(".col-md-3");
    
        // Lógica de permisos según rol
        if (role === "admin") {
            // El administrador tiene acceso a todo
        } else if (role === "vendedor") {
            // El vendedor solo puede acceder a Productos y Ventas
            usuariosLink.style.display = "none";
            categoriasLink.style.display = "none";
            usuariosCard.style.display = "none";
            categoriasCard.style.display = "none";

              // Aplicamos estilos para centrar las cartas
        productosCard.style.display = "flex";
        productosCard.style.justifyContent = "center"; // Centrado horizontal
        productosCard.style.alignItems = "center"; // Centrado vertical
        productosCard.style.margin = "0 auto"; // Asegura centrado horizontal

        ventasCard.style.display = "flex";
        ventasCard.style.justifyContent = "center"; // Centrado horizontal
        ventasCard.style.alignItems = "center"; // Centrado vertical
        ventasCard.style.margin = "0 auto"; // Asegura centrado horizontal


        
// Ajusta el origen al centro
        } else if (role === "client") {
            // El cliente solo puede acceder a Productos
            usuariosLink.style.display = "none";
            categoriasLink.style.display = "none";
            ventasLink.style.display = "none";
            usuariosCard.style.display = "none";
            categoriasCard.style.display = "none";
            ventasCard.style.display = "none";

            productosCard.style.display = "flex";
        productosCard.style.justifyContent = "center"; // Centrado horizontal
        productosCard.style.alignItems = "center"; // Centrado vertical
        productosCard.style.margin = "0 auto"; // 
            
        } else {
            alert("Rol no reconocido. Acceso denegado.");
            window.location.href = "login.html"; // Redirigir al login si el rol no es válido
        }
   
    if (!localStorage.getItem('reloaded')) {
        // Borrar y establecer el flag
        localStorage.clear();
        localStorage.setItem('reloaded', 'true');
        
        // Recargar la página
        location.reload();
    } else {
        // Eliminar el flag para futuras actualizaciones
        localStorage.removeItem('reloaded');
        console.log("El localStorage ha sido reiniciado y la página recargada.");
    }

    // Guardar datos simulados en el localStorage si no existen
    if (!localStorage.getItem("inventario")) {
        localStorage.setItem("inventario", JSON.stringify(sistemaInventario));
    }

    // Recuperar los datos del localStorage
    const inventario = JSON.parse(localStorage.getItem("inventario"));

    // Verificar si los datos existen en el localStorage
    if (inventario) {
        // Actualizar los contadores en la barra lateral
        document.getElementById("usuarios-count-sidebar").textContent = inventario.usuarios;
        document.getElementById("categorias-count-sidebar").textContent = inventario.categorias;
        document.getElementById("productos-count-sidebar").textContent = inventario.productos.length;
        document.getElementById("ventas-count-sidebar").textContent = inventario.ventas.length;

        // Actualizar los contadores del dashboard
        document.getElementById("usuarios-count").textContent = inventario.usuarios;
        document.getElementById("categorias-count").textContent = inventario.categorias;
        document.getElementById("productos-count").textContent = inventario.productos.length;
        document.getElementById("ventas-count").textContent = inventario.ventas.length;
    } else {
        console.warn("No se encontraron datos de inventario en el localStorage.");
    }
});


    window.onload = function() {
       
   
        document.getElementById('loading-screen').style.display = 'none'; // Ocultar la pantalla de carga
    };