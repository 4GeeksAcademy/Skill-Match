// Script para generar datos aleatorios para la API Skill-Match
// Este script crea usuarios, perfiles, skills, proyectos y propuestas con datos ficticios
// Para ejecutar: node seed_data.js

const fetch = (...args) =>
  import("node-fetch").then(({ default: fetch }) => fetch(...args));

// URL base de la API
const API_URL = "http://localhost:3001/api";

// Arrays con datos aleatorios para generar contenido
const freelancerNames = [
  { first: "Juan", last: "Pérez" },
  { first: "Ana", last: "García" },
  { first: "Carlos", last: "Rodríguez" },
  { first: "María", last: "López" },
  { first: "Diego", last: "Martínez" },
  { first: "Laura", last: "Sánchez" },
  { first: "Alejandro", last: "González" },
  { first: "Sofía", last: "Fernández" },
  { first: "Pablo", last: "Díaz" },
  { first: "Lucía", last: "Torres" },
  { first: "Miguel", last: "Ramírez" },
  { first: "Valentina", last: "Morales" },
];

const employerNames = [
  { first: "Roberto", last: "Méndez" },
  { first: "Gabriela", last: "Vargas" },
  { first: "José", last: "Herrera" },
  { first: "Claudia", last: "Castro" },
  { first: "Fernando", last: "Gutiérrez" },
  { first: "Silvia", last: "Ortiz" },
  { first: "Antonio", last: "Romero" },
  { first: "Patricia", last: "Jiménez" },
];

const companyNames = [
  "TechSolutions SpA",
  "Digital Innovators",
  "CodeMasters",
  "WebFuture",
  "AppCreations",
  "DataSmart",
  "DevExpress",
  "CloudNinjas",
];

const profileBios = [
  "Desarrollador full-stack con amplia experiencia en JavaScript y Python. Especializado en React y Node.js.",
  "Diseñadora UX/UI enfocada en crear experiencias intuitivas y atractivas. Manejo avanzado de Adobe XD y Figma.",
  "Desarrollador backend con experiencia en arquitecturas escalables. Especialista en Python, Django y bases de datos.",
  "Experta en desarrollo frontend, con dominio de HTML5, CSS3 y frameworks modernos como React y Vue.",
  "Analista de datos con conocimientos en Python, R y SQL. Experiencia en visualización de datos y machine learning.",
  "DevOps engineer con amplio conocimiento en AWS, Docker y CI/CD. Automatización de procesos y optimización de infraestructura.",
  "Desarrollador móvil especializado en React Native y Flutter. Creación de aplicaciones multiplataforma de alto rendimiento.",
  "Especialista en seguridad informática con experiencia en auditorías, pentesting y soluciones de seguridad.",
  "Full-stack developer con más de 5 años de experiencia creando aplicaciones web completas y escalables.",
  "Desarrollador de juegos con experiencia en Unity y Unreal Engine. Especialista en gráficos 3D y mecánicas de juego.",
  "Ingeniero de IA con experiencia en desarrollo de modelos de machine learning y procesamiento de lenguaje natural.",
  "Experto en cloud computing especializado en soluciones empresariales en AWS, Azure y Google Cloud.",
];

const skills = [
  "JavaScript",
  "Python",
  "React",
  "Node.js",
  "Angular",
  "Vue.js",
  "Django",
  "Flask",
  "SQL",
  "MongoDB",
  "AWS",
  "Docker",
  "TypeScript",
  "PHP",
  "Ruby",
  "C#",
  ".NET",
  "HTML5",
  "CSS3",
  "SASS",
  "Redux",
  "GraphQL",
  "REST API",
  "Java",
  "Spring Boot",
  "Kotlin",
  "Swift",
  "React Native",
  "Flutter",
  "Firebase",
  "Kubernetes",
  "CI/CD",
  "Git",
  "Figma",
  "Adobe XD",
  "Sketch",
  "Illustrator",
  "Photoshop",
  "UI/UX",
  "SEO",
  "Content Marketing",
  "Digital Marketing",
  "Data Analysis",
  "Machine Learning",
  "TensorFlow",
  "PyTorch",
  "Natural Language Processing",
  "Computer Vision",
];

const projectCategories = [
  "web-development",
  "mobile-development",
  "ui-ux-design",
  "data-science",
  "devops",
  "security",
  "marketing",
  "content-creation",
  "e-commerce",
  "game-development",
];

const projectTitles = [
  "Desarrollo de tienda online para empresa de moda",
  "Creación de aplicación móvil de entrega a domicilio",
  "Rediseño de sitio web corporativo",
  "Sistema de gestión de inventario para PYME",
  "Implementación de chatbot para servicio al cliente",
  "Desarrollo de dashboard para análisis de datos",
  "Aplicación web para gestión de proyectos",
  "Plataforma de reservas para restaurante",
  "Desarrollo de blog corporativo",
  "Sistema de gestión de contenidos personalizado",
  "Aplicación de seguimiento de gastos personales",
  "Plataforma educativa en línea",
  "Desarrollo de API para integración con proveedores",
  "Creación de landing page para producto nuevo",
  "Implementación de pasarela de pagos en sitio existente",
  "Sistema de registro y autenticación para aplicación web",
  "Desarrollo de red social interna para empresa",
  "Aplicación para gestión de recursos humanos",
  "Plataforma de streaming para eventos en vivo",
  "Sistema de reservas para clínica médica",
];

const projectDescriptions = [
  "Buscamos desarrollar una tienda online completa con catálogo de productos, carrito de compras, pasarela de pagos y sistema de gestión de inventario.",
  "Necesitamos una aplicación móvil (iOS y Android) que permita a los usuarios pedir productos a domicilio, con seguimiento en tiempo real y sistema de notificaciones.",
  "Queremos rediseñar completamente nuestro sitio web corporativo para mejorar la experiencia de usuario, optimizar la velocidad y adaptarlo a dispositivos móviles.",
  "Necesitamos un sistema que nos permita gestionar nuestro inventario, con alertas de stock, generación de informes y gestión de proveedores.",
  "Buscamos implementar un chatbot en nuestro sitio web que pueda responder preguntas frecuentes, guiar a los usuarios y derivar a un agente humano cuando sea necesario.",
  "Necesitamos una herramienta visual que muestre en tiempo real métricas clave del negocio, con gráficos interactivos y alertas configurables.",
  "Queremos desarrollar una aplicación web que permita la gestión completa de proyectos, con asignación de tareas, seguimiento de tiempo y generación de informes.",
  "Buscamos una plataforma que permita a nuestros clientes reservar mesa en nuestro restaurante, con sistema de notificaciones y gestión de disponibilidad.",
  "Necesitamos desarrollar un blog corporativo con sistema de categorías, tags, comentarios y newsletter integrado.",
  "Buscamos un CMS personalizado que se adapte a las necesidades específicas de nuestra empresa, permitiendo la gestión de contenidos de forma sencilla.",
  "Queremos una aplicación que permita al usuario registrar y categorizar sus gastos, generar informes y establecer presupuestos mensuales.",
  "Necesitamos una plataforma para impartir cursos en línea, con sistema de lecciones, exámenes, foros y certificados.",
  "Buscamos desarrollar una API REST que permita la integración con nuestros proveedores, sincronizando inventario y precios.",
  "Necesitamos una landing page atractiva y optimizada para conversión para el lanzamiento de nuestro nuevo producto.",
  "Queremos implementar una pasarela de pagos en nuestro sitio web existente, con soporte para múltiples medios de pago y suscripciones.",
  "Buscamos desarrollar un sistema de registro y autenticación seguro, con verificación de email, recuperación de contraseña y autenticación en dos pasos.",
  "Necesitamos una red social interna para nuestra empresa, que facilite la comunicación y colaboración entre departamentos.",
  "Queremos una aplicación que permita gestionar todos los procesos de RRHH, desde contratación hasta evaluación de desempeño.",
  "Buscamos una plataforma que permita transmitir eventos en vivo a cientos de usuarios simultáneamente, con chat en tiempo real.",
  "Necesitamos un sistema de reservas para nuestra clínica, donde los pacientes puedan agendar citas con diferentes especialistas.",
];

const profilePictures = [
  "https://randomuser.me/api/portraits/men/1.jpg",
  "https://randomuser.me/api/portraits/women/2.jpg",
  "https://randomuser.me/api/portraits/men/3.jpg",
  "https://randomuser.me/api/portraits/women/4.jpg",
  "https://randomuser.me/api/portraits/men/5.jpg",
  "https://randomuser.me/api/portraits/women/6.jpg",
  "https://randomuser.me/api/portraits/men/7.jpg",
  "https://randomuser.me/api/portraits/women/8.jpg",
  "https://randomuser.me/api/portraits/men/9.jpg",
  "https://randomuser.me/api/portraits/women/10.jpg",
  "https://randomuser.me/api/portraits/men/11.jpg",
  "https://randomuser.me/api/portraits/women/12.jpg",
];

const proposalMessages = [
  "Me interesa mucho este proyecto ya que tengo experiencia previa en proyectos similares. Podría entregar un trabajo de calidad en el plazo establecido.",
  "Considero que mi perfil se ajusta perfectamente a las necesidades de este proyecto. Tengo amplia experiencia en las tecnologías mencionadas.",
  "He trabajado en varios proyectos parecidos a este y puedo aportar ideas innovadoras para conseguir el mejor resultado posible.",
  "Mi experiencia en el sector me permite entender perfectamente las necesidades del proyecto y ofrecer una solución óptima.",
  "Estoy muy interesado en colaborar en este proyecto. Mi conocimiento técnico y mi enfoque en la calidad serían de gran valor.",
  "He revisado detalladamente los requisitos del proyecto y estoy seguro de que puedo cumplir con todas las expectativas en tiempo y forma.",
  "Me especializo exactamente en este tipo de desarrollos y puedo ofrecer un trabajo profesional y de alta calidad.",
  "Estoy disponible para comenzar de inmediato y completar el proyecto en el tiempo requerido. Mi experiencia me permite trabajar de forma eficiente.",
  "Mi portfolio incluye proyectos similares con excelentes resultados. Me encantaría discutir más detalles sobre este proyecto.",
  "Cuento con todas las habilidades necesarias para este proyecto y puedo ofrecer un precio competitivo sin comprometer la calidad.",
];

// Función para generar un número aleatorio entre min y max (ambos inclusive)
function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Función para generar una fecha aleatoria en el futuro (entre 1 y maxMonths meses)
function getRandomFutureDate(maxMonths = 6) {
  const today = new Date();
  const futureDate = new Date(today);
  futureDate.setMonth(today.getMonth() + getRandomInt(1, maxMonths));
  return futureDate.toISOString().split("T")[0]; // Formato YYYY-MM-DD
}

// Función para elegir n elementos aleatorios de un array
function getRandomElements(array, n) {
  const shuffled = [...array].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, n);
}

// Función genérica para realizar solicitudes a la API
async function apiRequest(endpoint, method = "GET", data = null) {
  const headers = { "Content-Type": "application/json" };
  const options = { method, headers };

  if (data) {
    options.body = JSON.stringify(data);
  }

  try {
    console.log(`Realizando solicitud ${method} a ${API_URL}${endpoint}`);
    const response = await fetch(`${API_URL}${endpoint}`, options);

    // Verificar estado de la respuesta
    if (!response.ok) {
      console.error(`Error HTTP: ${response.status} ${response.statusText}`);

      // Intentar obtener más información del error
      const contentType = response.headers.get("content-type");
      if (contentType && contentType.includes("text/html")) {
        const text = await response.text();
        console.error(
          `Respuesta HTML recibida, primeros 150 caracteres: ${text.substring(
            0,
            150
          )}...`
        );
        throw new Error(
          `Error de servidor en ${endpoint}: respuesta HTML recibida`
        );
      }

      try {
        const errorJson = await response.json();
        console.error("Detalles del error:", errorJson);
        throw new Error(
          `Error de servidor en ${endpoint}: ${JSON.stringify(errorJson)}`
        );
      } catch (jsonError) {
        const text = await response.text();
        console.error(
          `Error de servidor, respuesta: ${text.substring(0, 150)}...`
        );
        throw new Error(`Error de servidor en ${endpoint}: ${response.status}`);
      }
    }

    // Verificar el tipo de contenido
    const contentType = response.headers.get("content-type");
    if (!contentType || !contentType.includes("application/json")) {
      console.warn(`Advertencia: La respuesta no es JSON (${contentType})`);
      const text = await response.text();
      console.warn(
        `Respuesta recibida (primeros 150 caracteres): ${text.substring(
          0,
          150
        )}...`
      );
      throw new Error(`Respuesta no es JSON: ${contentType}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`Error en la solicitud a ${endpoint}:`, error.message);
    if (method === "POST") {
      console.error("Datos enviados:", JSON.stringify(data, null, 2));
    }
    return null;
  }
}

// Función para obtener todas las skills
async function getAllSkills() {
  return await apiRequest("/skills");
}

// Función para obtener todos los usuarios
async function getAllUsers() {
  // Usar la ruta correcta del backend
  return await apiRequest("/admin/users");
}

// Función para obtener todos los proyectos
async function getAllProjects() {
  return await apiRequest("/projects");
}

// Función para crear un usuario (freelancer o empleador)
async function createUser(email, password, role, firstName, lastName) {
  const userData = {
    email,
    password,
    role,
    first_name: firstName,
    last_name: lastName,
  };

  return await apiRequest("/register", "POST", userData);
}

// Función para crear un perfil de freelancer
async function createFreelancerProfile(
  userId,
  bio,
  profilePicture,
  hourlyRate
) {
  const profileData = {
    user_id: userId,
    bio,
    profile_picture: profilePicture,
    hourly_rate: hourlyRate,
  };

  return await apiRequest("/freelancer/profile", "POST", profileData);
}

// Función para asignar skills a un freelancer
async function assignSkillsToFreelancer(userId, skillIds) {
  const data = {
    user_id: userId,
    skill_ids: skillIds,
  };

  return await apiRequest("/freelancer/skills", "POST", data);
}

// Función para crear un proyecto
async function createProject(
  employerId,
  title,
  description,
  category,
  budget,
  deadline
) {
  // Asegurar que la fecha tenga el formato correcto YYYY-MM-DD
  const formattedDeadline = new Date(deadline).toISOString().split("T")[0];

  const projectData = {
    employer_id: employerId,
    title,
    description,
    category,
    budget,
    deadline: formattedDeadline,
  };

  return await apiRequest("/projects", "POST", projectData);
}

// Función para crear una propuesta para un proyecto
async function createProposal(
  projectId,
  freelancerId,
  message,
  proposedBudget
) {
  const proposalData = {
    freelancer_id: freelancerId,
    message,
    proposed_budget: proposedBudget,
  };

  return await apiRequest(
    `/projects/${projectId}/proposals`,
    "POST",
    proposalData
  );
}

// Función principal para generar todos los datos
async function generateData() {
  console.log("=== INICIANDO GENERACIÓN DE DATOS ALEATORIOS ===");

  // 0. Verificar datos existentes
  console.log("\n0. Verificando datos existentes...");

  // Obtener skills existentes
  let existingSkills = await getAllSkills();
  if (!existingSkills) existingSkills = [];
  console.log(`Encontradas ${existingSkills.length} skills existentes`);

  // Obtener usuarios existentes
  let existingUsers = await getAllUsers();
  if (!existingUsers) existingUsers = [];
  console.log(`Encontrados ${existingUsers.length} usuarios existentes`);

  // Separar usuarios por rol
  const existingFreelancers = existingUsers.filter(
    (user) => user.role === "freelancer"
  );
  const existingEmployers = existingUsers.filter(
    (user) => user.role === "employer"
  );
  console.log(`- Freelancers: ${existingFreelancers.length}`);
  console.log(`- Empleadores: ${existingEmployers.length}`);

  // Obtener proyectos existentes
  let existingProjects = await getAllProjects();
  if (!existingProjects) existingProjects = [];
  console.log(`Encontrados ${existingProjects.length} proyectos existentes`);

  // 1. Crear skills (solo las que no existen)
  console.log("\n1. Creando skills...");
  const createdSkills = [...existingSkills];

  for (const skillName of skills) {
    // Verificar si la skill ya existe
    const existingSkill = existingSkills.find((s) => s.name === skillName);
    if (existingSkill) {
      console.log(`Skill "${skillName}" ya existe, omitiendo creación`);
      continue;
    }

    const skill = await apiRequest("/skills", "POST", { name: skillName });
    if (skill && skill.id) {
      createdSkills.push(skill);
    }
  }

  console.log(`✅ Total de skills disponibles: ${createdSkills.length}`);

  // 2. Crear usuarios freelancers (solo los que no existen)
  console.log("\n2. Creando usuarios freelancers...");
  const createdFreelancers = [...existingFreelancers];

  for (const name of freelancerNames) {
    const email = `${name.first.toLowerCase()}.${name.last.toLowerCase()}@example.com`;

    // Verificar si el usuario ya existe
    const existingUser = existingUsers.find((u) => u.email === email);
    if (existingUser) {
      console.log(`Usuario con email "${email}" ya existe, omitiendo creación`);
      if (
        existingUser.role === "freelancer" &&
        !createdFreelancers.includes(existingUser)
      ) {
        createdFreelancers.push(existingUser);
      }
      continue;
    }

    const user = await createUser(
      email,
      "password123",
      "freelancer",
      name.first,
      name.last
    );

    if (user && user.id) {
      createdFreelancers.push(user);

      // Crear perfil para este freelancer
      const randomBio = profileBios[getRandomInt(0, profileBios.length - 1)];
      const randomPicture =
        profilePictures[getRandomInt(0, profilePictures.length - 1)];
      const hourlyRate = getRandomInt(15, 80);

      const profile = await createFreelancerProfile(
        user.id,
        randomBio,
        randomPicture,
        hourlyRate
      );

      // Asignar entre 3 y 6 skills aleatorias a este freelancer
      const randomSkillCount = getRandomInt(3, 6);
      const randomSkillIds = getRandomElements(
        createdSkills,
        randomSkillCount
      ).map((skill) => skill.id);
      await assignSkillsToFreelancer(user.id, randomSkillIds);
    }
  }

  console.log(
    `✅ Total de freelancers disponibles: ${createdFreelancers.length}`
  );

  // 3. Crear usuarios empleadores (solo los que no existen)
  console.log("\n3. Creando usuarios empleadores...");
  const createdEmployers = [...existingEmployers];

  for (let i = 0; i < employerNames.length; i++) {
    const name = employerNames[i];
    const companyName = companyNames[i % companyNames.length];
    const email = `${name.first.toLowerCase()}.${name.last.toLowerCase()}@${companyName
      .toLowerCase()
      .replace(/\s+/g, "-")}.com`;

    // Verificar si el usuario ya existe
    const existingUser = existingUsers.find((u) => u.email === email);
    if (existingUser) {
      console.log(`Usuario con email "${email}" ya existe, omitiendo creación`);
      if (
        existingUser.role === "employer" &&
        !createdEmployers.includes(existingUser)
      ) {
        createdEmployers.push(existingUser);
      }
      continue;
    }

    const user = await createUser(
      email,
      "password123",
      "employer",
      name.first,
      name.last
    );

    if (user && user.id) {
      createdEmployers.push(user);
    }
  }

  console.log(`✅ Total de empleadores disponibles: ${createdEmployers.length}`);

  // 4. Crear proyectos (solo los que no existen)
  console.log("\n4. Creando proyectos...");
  const createdProjects = [...existingProjects];

  // Crear un mapa de títulos de proyectos existentes para búsqueda rápida
  const existingProjectTitles = new Set(existingProjects.map((p) => p.title));

  for (let i = 0; i < projectTitles.length; i++) {
    const title = projectTitles[i];

    // Verificar si el proyecto ya existe
    if (existingProjectTitles.has(title)) {
      console.log(`Proyecto "${title}" ya existe, omitiendo creación`);
      continue;
    }

    if (createdEmployers.length === 0) {
      console.log("No hay empleadores disponibles para crear proyectos");
      break;
    }

    const employerId = createdEmployers[i % createdEmployers.length].id;
    const description = projectDescriptions[i % projectDescriptions.length];
    const category =
      projectCategories[getRandomInt(0, projectCategories.length - 1)];
    const budget = getRandomInt(500, 10000);
    const deadline = getRandomFutureDate(6);

    const project = await createProject(
      employerId,
      title,
      description,
      category,
      budget,
      deadline
    );

    if (project && project.id) {
      createdProjects.push(project);
    }
  }

  console.log(`✅ Total de proyectos disponibles: ${createdProjects.length}`);

  // 5. Crear propuestas para los proyectos (sin duplicar)
  console.log("\n5. Creando propuestas para los proyectos...");
  let totalProposals = 0;

  // Obtener propuestas existentes para cada proyecto
  for (const project of createdProjects) {
    // Obtener propuestas existentes para este proyecto
    const existingProposals = await apiRequest(
      `/projects/${project.id}/proposals`
    );
    const existingFreelancerIds = existingProposals
      ? existingProposals.map((p) => p.freelancer_id)
      : [];
    console.log(
      `Proyecto ${project.id} tiene ${existingFreelancerIds.length} propuestas existentes`
    );

    // Generar entre 1 y 5 propuestas por proyecto
    const proposalCount = getRandomInt(1, 5);
    const availableFreelancers = createdFreelancers.filter(
      (freelancer) => !existingFreelancerIds.includes(freelancer.id)
    );

    if (availableFreelancers.length === 0) {
      console.log(
        `No hay freelancers disponibles para propuestas en el proyecto ${project.id}`
      );
      continue;
    }

    const randomFreelancers = getRandomElements(
      availableFreelancers,
      Math.min(proposalCount, availableFreelancers.length)
    );

    for (const freelancer of randomFreelancers) {
      const message =
        proposalMessages[getRandomInt(0, proposalMessages.length - 1)];
      const proposedBudget = getRandomInt(
        Math.round(project.budget * 0.7),
        project.budget
      );

      const proposal = await createProposal(
        project.id,
        freelancer.id,
        message,
        proposedBudget
      );

      if (proposal) {
        totalProposals++;
      }
    }
  }

  console.log(`✅ Creadas ${totalProposals} propuestas nuevas`);

  console.log("\n=== GENERACIÓN DE DATOS COMPLETADA ===");
  console.log("\nResumen:");
  console.log(`- Skills: ${createdSkills.length}`);
  console.log(`- Freelancers: ${createdFreelancers.length}`);
  console.log(`- Empleadores: ${createdEmployers.length}`);
  console.log(`- Proyectos: ${createdProjects.length}`);
  console.log(`- Propuestas: ${totalProposals} nuevas`);
  console.log(
    "\nLos datos están listos para ser utilizados por el equipo de frontend."
  );
}

// Ejecutar la función principal
generateData().catch((error) => {
  console.error("Error durante la generación de datos:", error);
});
