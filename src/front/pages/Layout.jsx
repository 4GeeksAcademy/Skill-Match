import ScrollToTop from "../components/ScrollToTop"
import { Navbar } from "../components/Navbar"
import { Jumbotron } from "../components/Jumbotron"
import { Footer } from "../components/Footer"
import { LittleCards } from "../components/LittleCards"
import { Outlet } from 'react-router-dom';
import React from 'react'

// Base component that maintains the navbar and footer throughout the page and the scroll to top functionality.
export const Layout = () => {
    return (



        <div>
            <ScrollToTop>
                <Navbar />
               

                <div className="content">
                    <Outlet />
                </div>
               

                <Footer />
            </ScrollToTop>
        </div>


    )
}