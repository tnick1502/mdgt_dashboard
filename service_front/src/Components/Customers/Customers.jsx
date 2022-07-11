import React, { useContext, useState, useEffect, useRef } from 'react'

import './Customers.css'

import Context from '../../context'
import NotLogged from '../NotLogged/NotLogged'
import stock from './stock.png'
import Loader from '../Loader/Loader'

export default function Customers() {
	const { isLogged, api_customers } = useContext(Context)
	const [customers, setCustomers] = useState([{}])

	const [loaded, setLoaded] = useState(false)

	const currentMonth = useRef(new Date().getMonth() + 1)

	useEffect(() => {
		if (!isLogged) {
			setLoaded(false)
			setCustomers([{}])
			return
		}

		function updateCustomers() {
			if (isLogged) {
				fetch(
					`${api_customers}customers/month_birthday/?month=${currentMonth.current}`
				)
					.then((response) => response.json())
					.then((data) => {
						if (data && data.length > 0) {
							setCustomers(data)
							setLoaded(true)
						}
					})
			}
		}

		updateCustomers()
	}, [isLogged])

	function getImg(id) {
		return `${api_customers}customers/get_photo/${id}`
	}

	return (
		<>
			<React.Fragment>
				{isLogged ? (
					<div className="card-item customers-item">
						{loaded ? (
							<>
								<h1 className="customers-table__caption">
									Дни рождения заказчиков
								</h1>
								<div className="customers-table__wrapper">
									<table className="customers-table">
										<thead className="customers-table__head">
											<tr>
												<th scope="col">Имя</th>
												<th className="date" scope="col">
													Дата
												</th>
												<th scope="col">Организация</th>
												<th className="phone" scope="col">
													Телефон
												</th>
											</tr>
										</thead>
										<tbody>
											{customers.map((customer) => (
												<tr className="customers-table__row" key={customer.id}>
													<td>
														<div className="customer__name">
															<img
																className="customer__icon"
																src={getImg(customer.id)}
																alt="User"
																onError={({ currentTarget }) => {
																	currentTarget.onerror = null // prevents looping
																	currentTarget.src = stock
																}}
															></img>
															{customer.full_name}
														</div>
													</td>
													<td className="date">{customer.birthday}</td>
													<td>{customer.organization}</td>
													<td className="phone">{customer.phone_number}</td>
												</tr>
											))}
										</tbody>
									</table>
								</div>
							</>
						) : (
							<Loader />
						)}
					</div>
				) : (
					<NotLogged />
				)}
			</React.Fragment>
		</>
	)
}
