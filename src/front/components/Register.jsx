import React, { useState } from 'react';

const Register = () => {
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        company: '',
        gender: '',
        age: '',
        error: ''
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value
        }));
    };


    const handleSubmit = (e) => {
        e.preventDefault();


        const { firstName, lastName, email, password, company, gender, age } = formData;

        if (!firstName || !lastName || !email || !password || !company || !gender || !age) {
            setFormData((prevData) => ({ ...prevData, error: 'Por favor, completa todos los campos.' }));
            return;
        }

        if (!/\S+@\S+\.\S+/.test(email)) {
            setFormData((prevData) => ({ ...prevData, error: 'Por favor, ingresa un correo electrónico válido.' }));
            return;
        }

        if (password.length < 6) {
            setFormData((prevData) => ({ ...prevData, error: 'La contraseña debe tener al menos 6 caracteres.' }));
            return;
        }


        console.log('Datos enviados:', formData);


        history.push('/login');
    };

    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-6">
                    <div className="card">
                        <div className="card-body">
                            <h3 className="card-title text-center">Crear Cuenta</h3>
                            {formData.error && <div className="alert alert-danger">{formData.error}</div>}
                            <form onSubmit={handleSubmit}>
                                <div className="mb-3">
                                    <label htmlFor="firstName" className="form-label">Nombres</label>
                                    <input
                                        type="text"
                                        id="firstName"
                                        className="form-control"
                                        placeholder="Ingrese sus nombres"
                                        name="firstName"
                                        value={formData.firstName}
                                        onChange={handleChange}
                                    />
                                </div>

                                <div className="mb-3">
                                    <label htmlFor="lastName" className="form-label">Apellidos</label>
                                    <input
                                        type="text"
                                        id="lastName"
                                        className="form-control"
                                        placeholder="Ingrese sus apellidos"
                                        name="lastName"
                                        value={formData.lastName}
                                        onChange={handleChange}
                                    />
                                </div>

                                <div className="mb-3">
                                    <label htmlFor="email" className="form-label">Correo Electrónico</label>
                                    <input
                                        type="email"
                                        id="email"
                                        className="form-control"
                                        placeholder="Ingrese su correo electrónico"
                                        name="email"
                                        value={formData.email}
                                        onChange={handleChange}
                                    />
                                </div>

                                <div className="mb-3">
                                    <label htmlFor="password" className="form-label">Contraseña</label>
                                    <input
                                        type="password"
                                        id="password"
                                        className="form-control"
                                        placeholder="Ingrese una contraseña"
                                        name="password"
                                        value={formData.password}
                                        onChange={handleChange}
                                    />
                                </div>

                                <div className="mb-3">
                                    <label htmlFor="company" className="form-label">Empresa (Opcional)</label>
                                    <input
                                        type="text"
                                        id="company"
                                        className="form-control"
                                        placeholder="Ingrese el nombre de su empresa (si aplica)"
                                        name="company"
                                        value={formData.company}
                                        onChange={handleChange}
                                    />
                                </div>

                                <div className="mb-3">
                                    <label htmlFor="gender" className="form-label">Género</label>
                                    <select
                                        id="gender"
                                        className="form-select"
                                        name="gender"
                                        value={formData.gender}
                                        onChange={handleChange}
                                    >
                                        <option value="">Seleccione su género</option>
                                        <option value="male">Masculino</option>
                                        <option value="female">Femenino</option>
                                        <option value="other">Otro</option>
                                    </select>
                                </div>

                                <div className="mb-3">
                                    <label htmlFor="age" className="form-label">Edad</label>
                                    <input
                                        type="number"
                                        id="age"
                                        className="form-control"
                                        placeholder="Ingrese su edad"
                                        name="age"
                                        value={formData.age}
                                        onChange={handleChange}
                                    />
                                </div>

                                <button type="submit" className="btn btn-dark w-100">
                                    Registrarse
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Register;
