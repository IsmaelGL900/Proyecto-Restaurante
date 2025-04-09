function ocultarContraseñas() {
        const passwordInput = document.getElementById("password");
      const toggleIcon = document.getElementById("toggleIcon");

      if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleIcon.src = "{% static 'Imagenes/ojo-abierto.png' %}";
      } else {
        passwordInput.type = "password";
        toggleIcon.src = "{% static 'Imagenes/ojo-cerrado.png' %}";
      }
    }