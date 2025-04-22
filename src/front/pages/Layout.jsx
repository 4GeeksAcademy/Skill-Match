import { Outlet } from "react-router-dom/dist"
import ScrollToTop from "../components/ScrollToTop"
import { Navbar } from "../components/Navbar"
import { Jumbotron } from "../components/Jumbotron"
import { Footer } from "../components/Footer"
import { LittleCards } from "../components/LittleCards"

// Base component that maintains the navbar and footer throughout the page and the scroll to top functionality.
export const Layout = () => {
    return (
        <ScrollToTop>
            <Navbar />
            <Jumbotron />
                <Outlet />
            <h1 className="container my-4">Browse by category</h1>
            <div className="container d-flex justify-content-between">
                <LittleCards /><LittleCards /><LittleCards />
            </div>
            <Footer />
        </ScrollToTop>
    )
}