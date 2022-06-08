import React from 'react'
import { Routes, Route, NavLink } from 'react-router-dom'

import './Navigation.css'

import Summary from '../Summary/Summary'
import Prize from '../Prize/Prize'
import Reports from '../Reports/Reports'
import Payments from '../Payments/Payments'
import NotFound from '../NotFound/NotFound'
import { useState } from 'react'
import { useEffect } from 'react'
import useWindowDimensions from '../windowResizeHook'
import { useRef } from 'react'

export default function Navigation() {
	const [collapsed, setCollapsed] = useState(false)
	const forceCollapsed = useRef(false)

	function onExpandBtn() {
		forceCollapsed.current = true
		setCollapsed(!collapsed)
	}

	const { width } = useWindowDimensions()

	useEffect(() => {
		if (forceCollapsed.current) return
		if (width <= 768) {
			setCollapsed(true)
		} else {
			setCollapsed(false)
		}
	}, [width])

	return (
		<>
			<nav className="navigation card-item">
				<NavLink
					to="/"
					className={({ isActive }) =>
						isActive ? 'nav-link is-active' : 'nav-link'
					}
					title="Сводка"
				>
					<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24">
						<path d="M4 13h6a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1zm-1 7a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-4a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v4zm10 0a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-7a1 1 0 0 0-1-1h-6a1 1 0 0 0-1 1v7zm1-10h6a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1h-6a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1z"></path>
					</svg>
					{collapsed ? null : 'Сводка'}
				</NavLink>
				<NavLink
					to="/Prize"
					className={({ isActive }) =>
						isActive ? 'nav-link is-active' : 'nav-link'
					}
					title="Премия"
				>
					<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24">
						<path d="M21 4h-3V3a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1v1H3a1 1 0 0 0-1 1v3c0 4.31 1.8 6.91 4.82 7A6 6 0 0 0 11 17.91V20H9v2h6v-2h-2v-2.09A6 6 0 0 0 17.18 15c3-.1 4.82-2.7 4.82-7V5a1 1 0 0 0-1-1zM4 8V6h2v6.83C4.22 12.08 4 9.3 4 8zm14 4.83V6h2v2c0 1.3-.22 4.08-2 4.83z"></path>
					</svg>
					{collapsed ? null : 'Премия'}
				</NavLink>
				<NavLink
					to="/Reports"
					className={({ isActive }) =>
						isActive ? 'nav-link is-active' : 'nav-link'
					}
					title="Отчёты"
				>
					<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24">
						<path d="m20 8-6-6H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM9 19H7v-9h2v9zm4 0h-2v-6h2v6zm4 0h-2v-3h2v3zM14 9h-1V4l5 5h-4z"></path>
					</svg>
					{collapsed ? null : 'Отчёты'}
				</NavLink>
				<NavLink
					to="/Payments"
					className={({ isActive }) =>
						isActive ? 'nav-link is-active' : 'nav-link'
					}
					title="Выплаты"
				>
					<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24">
						<path d="M20 4H4c-1.103 0-2 .897-2 2v2h20V6c0-1.103-.897-2-2-2zM2 18c0 1.103.897 2 2 2h16c1.103 0 2-.897 2-2v-6H2v6zm3-3h6v2H5v-2z"></path>
					</svg>
					{collapsed ? null : 'Выплаты'}
				</NavLink>

				<button
					onClick={onExpandBtn}
					className="expand-collapse-btn"
					title={collapsed ? 'Развернуть' : 'Свернуть'}
				>
					{collapsed ? (
						<svg
							className="arrow-right"
							xmlns="http://www.w3.org/2000/svg"
							width="24"
							height="24"
						>
							<path d="M10.707 17.707 16.414 12l-5.707-5.707-1.414 1.414L13.586 12l-4.293 4.293z"></path>
						</svg>
					) : (
						<svg
							className="arrow-left"
							xmlns="http://www.w3.org/2000/svg"
							width="24"
							height="24"
						>
							<path d="M13.293 6.293 7.586 12l5.707 5.707 1.414-1.414L10.414 12l4.293-4.293z"></path>
						</svg>
					)}
				</button>
			</nav>

			<Routes>
				<Route path="/" element={<Summary />} />
				<Route path="/prize" element={<Prize />} />
				<Route path="/Reports" element={<Reports />} />
				<Route path="/Payments" element={<Payments />} />

				{/* 404 Page */}
				<Route path="*" element={<NotFound />} />
			</Routes>
		</>
	)
}
