import React, { useContext } from 'react'
import Context from '../../context'

import NotLogged from '../NotLogged/NotLogged'

import Prize from '../Prize/Prize'
import Reports from '../Reports/Reports'
import Payments from '../Payments/Payments'

import './Summary.css'

export default function Summary() {
	const { isLogged } = useContext(Context)

	return (
		<>
			{isLogged ? (
				<div className="transparent-item summary-flex">
					<Prize toSummary={true} />
					<Reports toSummary={true} />
					<Payments toSummary={true} />
				</div>
			) : (
				<NotLogged />
			)}
		</>
	)
}
