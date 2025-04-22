import { Link } from "react-router-dom";

export const Navbar = () => {

	return (
		<div className="container">
			<nav className="navbar">
  			<div className="container-fluid">
    			<a className="navbar-brand" href="#">
      				<img src="https://demo.themetorium.net/html/nui/assets/img/logo-dark.png" alt="Bootstrap" width="42" height="38"></img>
    			</a>
                <div className="navbar-nav navOptions col d-flex flex-row">
                	<a className="nav-link active me-3" aria-current="page" href="#">Home</a>
                	<a className="nav-link me-3" href="#">About</a>
                	<a className="nav-link me-3" href="#">Services</a>
                	<a className="nav-link" href="#">Contact</a>
              	</div>
				<form className="d-flex me-4" role="search">
        			<input className="form-control me-2" type="search" aria-label="Search"></input>
        			<button className="btn btn btn-outline-dark" type="submit" aria-label="Search"><i class="fa-solid fa-magnifying-glass"></i></button>
      			</form>
				<div>
					<a className="me-4">Log in</a>
					<Link to="/demo">
						<button type="button" class="btn btn-dark px-4 py-2">Sign up</button>
					</Link>
				</div>
  			</div>
			</nav>
		</div>
	);
};