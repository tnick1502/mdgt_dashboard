import React, { useContext, useState, useEffect } from 'react'
import Context from '../../context'
import './Reports.css'

import NotLogged from '../NotLogged/NotLogged'
import { parseReports } from '../utils'
import ReportsBarChart from './ReportsBarChart'
import ReportsDoughnut from './ReportsDoughnut'
import ReportsChart from './ReportsChart'

export default function Reports({ toSummary }) {
	const { isLogged, api } = useContext(Context)
	const [reports, setReports] = useState({ reports: [], dates: [] })

	const [reportsLoaded, setReportsLoaded] = useState(false)

	useEffect(() => {
		if (!isLogged) {
			setReportsLoaded(false)
			setReports({ reports: [], dates: [] })
			return
		}

		function updateReportsChart() {
			if (isLogged) {
				fetch(`${api}reports/`)
					.then((response) => response.json())
					.then((data) => {
						if (data && Object.keys(data).length > 0) {
							const resultData = parseReports(data)
							setReports(resultData)
							setReportsLoaded(true)
						}
					})
			}
		}

		updateReportsChart()

		const interval = setInterval(updateReportsChart, 100000)

		return () => {
			clearInterval(interval)
		}
	}, [isLogged])

	return (
		<>
			{toSummary ? (
				/* ФРАГМЕНТ ДЛЯ ЭКСПОРТА В SUMMARY */
				<React.Fragment>
					<div className="chart-card card-item chart-card_reports">
						<h1 className="">
							Выдано за {reports.dates[reports.dates.length - 1]}
						</h1>
						<div className="chart-card__chart">
							{reportsLoaded ? (
								<ReportsBarChart
									dataset={{
										reports: reports.reports[reports.reports.length - 1],
									}}
								/>
							) : (
								<div className="blank-page-ar-2"></div>
							)}
						</div>
					</div>
				</React.Fragment>
			) : (
				/* ФРАГМЕНТ СТРАНИЦЫ С ОТЧЕТАМИ */
				<React.Fragment>
					{isLogged ? (
						<div className="transparent-item reports-grid chart-card_reports">
							<div className="chart-card card-item">
								<h1 className="">
									Выдано за{' '}
									{reportsLoaded
										? reports.dates[reports.dates.length - 1]
										: null}
								</h1>
								<div className="chart-card__chart">
									{reportsLoaded ? (
										<ReportsBarChart
											dataset={{
												reports: reports.reports[reports.reports.length - 1],
											}}
										/>
									) : (
										<div className="blank-page-ar-2"></div>
									)}
								</div>
							</div>
							<div className="chart-card card-item reports-small-item">
								<h1 className="reports-small-item__title">
									Протоколы на Python
								</h1>
								<div className="reports-small-item__doughnut">
									{reportsLoaded ? (
										<ReportsDoughnut
											dataset={{
												reports: reports.reports[reports.reports.length - 1],
											}}
										/>
									) : (
										<div className="blank-page-ar-2"></div>
									)}
								</div>
							</div>
							<div className="chart-card card-item reports-small-item">
								<h1 className="reports-small-item__title">Статистика</h1>
								<div className="chart-card__chart ">
									{reportsLoaded ? (
										<ReportsChart
											dataset={{
												reports: reports.reports,
												dates: reports.dates,
											}}
										/>
									) : (
										<div className="blank-page-ar-2"></div>
									)}
								</div>
							</div>
						</div>
					) : (
						<NotLogged />
					)}
				</React.Fragment>
			)}
		</>
	)
}
