function handleCredentialResponse(response) {
  const data = parseJwt(response.credential);
  const email = data.email || "";
  const msg = document.getElementById("msg");
  const legajo = document.getElementById("legajo").value.trim();
  const emailInput = document.getElementById("emailInput");

  // Validación de legajo
  if (!legajo) {
    msg.textContent = "Por favor, ingresá tu número de legajo antes de continuar.";
    return;
  }

  // Validación de email institucional
  if (!email.endsWith("@fi.uba.ar")) {
    msg.textContent = "Solo se permiten correos institucionales (@fi.uba.ar).";
    return;
  }

  // Email válido → guardar y enviar
  msg.textContent = "Verificado correctamente. Bienvenido/a " + email + ".";
  emailInput.value = email;
  document.getElementById("registroForm").submit();
}

// Decodificador JWT para extraer el email
function parseJwt(token) {
  var base64Url = token.split('.')[1];
  var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));
  return JSON.parse(jsonPayload);
}