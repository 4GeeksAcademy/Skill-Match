import ScrollToTop from "../components/ScrollToTop"
import { Navbar } from "../components/Navbar"
import { Footer } from "../components/Footer"
import Register from "../components/Register"


// Base component that maintains the navbar and footer throughout the page and the scroll to top functionality.
export const Register = () => {
    return (
        <ScrollToTop>
            <Navbar />
            <Register />
            <Footer />
        </ScrollToTop>
    )
}