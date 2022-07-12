import React from 'react'

import NotLogged from '../NotLogged/NotLogged'

import Prize from '../Prize/Prize'
import Reports from '../Reports/Reports'
import Staff from '../Staff/Staff'
import Customers from '../Customers/Customers'

import './Summary.css'

export default function Summary() {
	// const { isLogged } = useContext(Context)
	const isLogged = true

	return (
		<>
			{isLogged ? (
				<>
					<div className="transparent-item summary-flex">
						<Prize toSummary={true} />
						<Staff />
						<Customers />
						<Reports toSummary={true} />
					</div>
				</>
			) : (
				<NotLogged />
			)}
		</>
	)
}
