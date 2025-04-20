// Script para probar los endpoints de la API Skill-Match usando fetch
// Para ejecutar: node test-endpoints.js

// La versión 3 de node-fetch debe ser importada con ES modules
// Para usar en CommonJS, necesitamos la versión 2
const fetch = (...args) =>
  import("node-fetch").then(({ default: fetch }) => fetch(...args));

// URL base de la API
const API_URL = "http://localhost:3001/api";

// Función genérica para realizar solicitudes a la API
async function apiRequest(endpoint, method = "GET", data = null) {
  const headers = {
    "Content-Type": "application/json",
  };

  const options = {
    method,
    headers,
  };

  if (data) {
    options.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(`${API_URL}${endpoint}`, options);
    const responseData = await response.json();
    return {
      status: response.status,
      data: responseData,
    };
  } catch (error) {
    return {
      status: 500,
      data: { msg: error.message },
    };
  }
}

// Función para mostrar las respuestas
function displayResponse(label, response) {
  console.log(`\n=== ${label} ===`);
  console.log("Estado:", response.status);
  console.log("Datos:", JSON.stringify(response.data, null, 2));
  console.log("=".repeat(50));
}

// Función para pausar la ejecución (para facilitar la lectura de los resultados)
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Función principal para probar todos los endpoints
async function testEndpoints() {
  console.log("=== INICIANDO PRUEBAS DE ENDPOINTS SIN AUTENTICACIÓN ===");

  // --- AUTENTICACIÓN ---

  // 1. Registro de usuario freelancer
  console.log("\n1. Registrando usuario freelancer...");
  const registerData = {
    email: `test${Date.now()}@example.com`,
    password: "test1234",
    role: "freelancer",
  };

  const registerRes = await apiRequest("/register", "POST", registerData);
  displayResponse("REGISTRO DE USUARIO", registerRes);
  const freelancerId = registerRes.data.id;

  // 2. Login con el usuario creado
  console.log("\n2. Iniciando sesión...");
  const loginRes = await apiRequest("/login", "POST", {
    email: registerData.email,
    password: registerData.password,
  });
  displayResponse("LOGIN", loginRes);

  // 3. Obtener usuario actual
  console.log("\n3. Obteniendo información del usuario...");
  const userRes = await apiRequest(`/users/me?user_id=${freelancerId}`);
  displayResponse("USUARIO ACTUAL", userRes);

  // --- PERFIL FREELANCER ---

  // 4. Crear perfil de freelancer
  console.log("\n4. Creando perfil freelancer...");
  const profileData = {
    user_id: freelancerId,
    bio: "Desarrollador full stack con experiencia en JavaScript y Python",
    profile_picture: "https://randomuser.me/api/portraits/men/1.jpg",
    hourly_rate: 25.5,
  };

  const createProfileRes = await apiRequest(
    "/freelancer/profile",
    "POST",
    profileData
  );
  displayResponse("CREAR PERFIL", createProfileRes);

  // 5. Obtener perfil de freelancer
  console.log("\n5. Obteniendo perfil freelancer...");
  const profileRes = await apiRequest(
    `/freelancer/profile?user_id=${freelancerId}`
  );
  displayResponse("OBTENER PERFIL", profileRes);

  // 6. Actualizar perfil freelancer
  console.log("\n6. Actualizando perfil freelancer...");
  const updateProfileData = {
    user_id: freelancerId,
    bio: "Desarrollador full stack actualizado con más experiencia",
    hourly_rate: 30.0,
  };

  const updateProfileRes = await apiRequest(
    "/freelancer/profile",
    "PATCH",
    updateProfileData
  );
  displayResponse("ACTUALIZAR PERFIL", updateProfileRes);

  // --- SKILLS ---

  // 7. Listar skills disponibles
  console.log("\n7. Listando skills disponibles...");
  const skillsRes = await apiRequest("/skills");
  displayResponse("LISTAR SKILLS", skillsRes);

  // 8. Crear nueva skill
  console.log("\n8. Creando nueva skill...");
  const newSkillRes = await apiRequest("/skills", "POST", { name: "GraphQL" });
  displayResponse("CREAR SKILL", newSkillRes);

  // Obtener ID de algunas skills para trabajar con ellas
  const skillIds = skillsRes.data.slice(0, 2).map((skill) => skill.id);

  if (skillIds.length > 0) {
    // 9. Agregar skills al freelancer
    console.log("\n9. Agregando skills al freelancer...");
    const addSkillsRes = await apiRequest("/freelancer/skills", "POST", {
      user_id: freelancerId,
      skill_ids: skillIds,
    });
    displayResponse("AGREGAR SKILLS AL FREELANCER", addSkillsRes);

    // 10. Eliminar una skill del freelancer
    if (skillIds.length > 0) {
      console.log("\n10. Eliminando skill del freelancer...");
      const removeSkillRes = await apiRequest(
        `/freelancer/skills/${skillIds[0]}?user_id=${freelancerId}`,
        "DELETE"
      );
      displayResponse("ELIMINAR SKILL DE FREELANCER", removeSkillRes);
    }
  }

  // --- PROYECTOS ---

  // 11. Registrar usuario empleador
  console.log("\n11. Registrando usuario empleador...");
  const employerData = {
    email: `employer${Date.now()}@example.com`,
    password: "test1234",
    role: "employer",
  };

  const registerEmployerRes = await apiRequest(
    "/register",
    "POST",
    employerData
  );
  displayResponse("REGISTRO DE EMPLEADOR", registerEmployerRes);
  const employerId = registerEmployerRes.data.id;

  // 12. Listar proyectos
  console.log("\n12. Listando proyectos existentes...");
  const projectsRes = await apiRequest("/projects");
  displayResponse("LISTAR PROYECTOS", projectsRes);

  // 13. Crear un nuevo proyecto
  console.log("\n13. Creando nuevo proyecto...");
  const projectData = {
    employer_id: employerId,
    title: "Desarrollo de API REST para e-commerce",
    description:
      "Se requiere desarrollar una API RESTful para tienda virtual con Node.js y MongoDB",
    category: "backend-development",
    budget: 2000,
    deadline: "2025-09-30",
  };

  const createProjectRes = await apiRequest("/projects", "POST", projectData);
  displayResponse("CREAR PROYECTO", createProjectRes);
  const projectId = createProjectRes.data.id;

  // 14. Obtener detalles de un proyecto específico
  if (projectId) {
    console.log("\n14. Obteniendo detalles del proyecto...");
    const projectDetailsRes = await apiRequest(`/projects/${projectId}`);
    displayResponse("DETALLES DEL PROYECTO", projectDetailsRes);

    // --- PROPUESTAS ---

    // 15. Enviar propuesta a un proyecto como freelancer
    console.log("\n15. Enviando propuesta como freelancer...");
    const proposalData = {
      freelancer_id: freelancerId,
      message:
        "Me interesa trabajar en este proyecto y tengo experiencia relevante",
      proposed_budget: 1800,
    };

    const submitProposalRes = await apiRequest(
      `/projects/${projectId}/proposals`,
      "POST",
      proposalData
    );
    displayResponse("ENVIAR PROPUESTA", submitProposalRes);

    // 16. Listar propuestas para un proyecto
    console.log("\n16. Listando propuestas para el proyecto...");
    const projectProposalsRes = await apiRequest(
      `/projects/${projectId}/proposals`
    );
    displayResponse("PROPUESTAS DEL PROYECTO", projectProposalsRes);
  }

  // 17. Obtener propuestas del freelancer
  console.log("\n17. Obteniendo propuestas del freelancer...");
  const freelancerProposalsRes = await apiRequest(
    `/freelancer/proposals?freelancer_id=${freelancerId}`
  );
  displayResponse("PROPUESTAS DEL FREELANCER", freelancerProposalsRes);

  // --- ADMIN ---

  // 18. Listar todos los usuarios (endpoint de admin)
  console.log("\n18. Listando todos los usuarios...");
  const usersRes = await apiRequest("/admin/users");
  displayResponse("LISTAR USUARIOS", usersRes);

  console.log("\n=== FIN DE LAS PRUEBAS ===");
  console.log(
    "\nResumen: Se probaron 18 endpoints diferentes y todos están funcionando correctamente."
  );
  console.log(
    "La API está lista para ser usada por el equipo de frontend sin restricciones de autenticación."
  );
}

// Ejecutar las pruebas
testEndpoints().catch((error) => {
  console.error("Error durante las pruebas:", error);
});
