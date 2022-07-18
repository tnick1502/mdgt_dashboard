import React, { useState, useRef, useEffect } from 'react'

import './App.css'

import LogInBar from './Components/LogInBar/LogInBar'
import Navigation from './Components/Navigation/Navigation'

import Context from './context'

function App() {
	const [isLogged, setLogged] = useState(false)
	const api = useRef('http://192.168.0.200:8000/')
	const api_customers = useRef('http://192.168.0.200:9000/')

	const [hidedCards, setHidedCards] = useState({})

	const [showScroll, setShowScroll] = useState(false)

	useEffect(() => {
		window.addEventListener('scroll', handleScroll)

		return () => {
			window.removeEventListener('scroll', handleScroll)
		}
	}, [])

	function handleScroll() {
		if (window.scrollY > 100) {
			setShowScroll(true)
		} else {
			setShowScroll(false)
		}
	}

	return (
		<>
			<Context.Provider
				value={{
					isLogged,
					setLogged,
					api: api.current,
					api_customers: api_customers.current,
					hidedCards,
					setHidedCards,
				}}
			>
				<div className="content-wrapper">
					<LogInBar />
					<div className="content">
						<Navigation />
					</div>
					<p className="footer__copy"> &#169; by MDGT </p>
				</div>
			</Context.Provider>

			<div
				class={showScroll ? 'scrolltop show-scroll' : 'scrolltop'}
				id="scroll-top"
				onClick={() => {
					window.scrollTo({ top: 0, left: 0, behavior: 'smooth' })
				}}
			>
				<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24">
					<path d="m6.293 13.293 1.414 1.414L12 10.414l4.293 4.293 1.414-1.414L12 7.586z"></path>
				</svg>
			</div>
		</>
	)
}

export default App
