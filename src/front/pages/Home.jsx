import React, { useEffect } from "react"
import { Jumbotron } from "../components/Jumbotron.jsx";
import { LittleCards } from "../components/LittleCards.jsx";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";

export const Home = () => {

	return (
		<div className="text-center mt-5">
			<Jumbotron />
			<h1 className="container my-4">Browse by category</h1>
			<div className="container d-flex justify-content-between">
				<LittleCards /><LittleCards /><LittleCards />
			</div>
		</div>
	);
}; 