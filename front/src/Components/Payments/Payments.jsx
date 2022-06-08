import React, { useContext, useEffect, useState } from 'react'
import Context from '../../context'
import axios from 'axios'

import './Payments.css'

import NotLogged from '../NotLogged/NotLogged'
import DisplayCard from '../DisplayCard/DisplayCard'
import PaymentsChart from './PaymentsChart'
import { parsePayments } from '../utils'

export default function Payments({ toSummary }) {
	const { isLogged, api } = useContext(Context)

	const [payments, setPayments] = useState({ payments: [], dates: [] })
	const [paymentsLoaded, setPaymentsLoaded] = useState(false)

	useEffect(() => {
		const instance2 = axios.create()
		instance2.interceptors.request.use(
			(config) => {
				// Код, необходимый до отправки запроса
				config.method = 'get'
				config.withCredentials = true
				return config
			},
			(error) => {
				// Обработка ошибки из запроса
				return Promise.reject(error)
			}
		)

		function updatePayments() {
			if (isLogged) {
				instance2
					.get(`${api}pay/`)
					.then((response) => response.data)
					.then((data) => {
						const resultData = parsePayments(data)
						setPayments(resultData)
						setPaymentsLoaded(true)
					})
			}
		}

		updatePayments()

		const interval = setInterval(updatePayments, 100000)

		return () => {
			clearInterval(interval)
		}
	}, [isLogged])

	return (
		<>
			{toSummary ? (
				<React.Fragment>
					<div className="chart-card card-item chart-card_payments">
						<h1 className="chart-card__header_">Динамика выплат</h1>
						<div className="chart-card__chart">
							{paymentsLoaded ? (
								<PaymentsChart
									dataset={{
										payments: payments.summ,
										dates: payments.dates,
									}}
								/>
							) : (
								<div className="blank-page-payments"></div>
							)}
						</div>
					</div>
				</React.Fragment>
			) : (
				<React.Fragment>
					{isLogged ? (
						<div className="transparent-item payments-grid unselectable">
							<div className="chart-card card-item chart-card_payments">
								<h1 className="chart-card__header_">Динамика выплат</h1>
								<div className="chart-card__chart">
									{paymentsLoaded ? (
										<PaymentsChart
											dataset={{
												payments: payments.summ,
												dates: payments.dates,
											}}
										/>
									) : (
										<div className="blank-page-payments"></div>
									)}
								</div>
							</div>
							{paymentsLoaded ? (
								<div className="display-cards-wrapper_payments">
									{Object.keys(payments.payments).map((element) => (
										<DisplayCard
											title={element}
											prize={
												payments.payments[element][
													payments.payments[element].length - 1
												]
											}
											date={
												payments.dates[payments.payments[element].length - 1]
											}
											chartLoaded={paymentsLoaded}
											key={element}
											closeBtn={true}
											id={element}
										/>
									))}
								</div>
							) : null}
						</div>
					) : (
						<NotLogged />
					)}
				</React.Fragment>
			)}
		</>
	)
}
