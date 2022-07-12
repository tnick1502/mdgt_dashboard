import React, { useContext, useState, useEffect } from 'react'
import Context from '../../context'
import './Reports.css'

import NotLogged from '../NotLogged/NotLogged'
import { parseReports } from '../utils'
import ReportsBarChart from './ReportsBarChart'
import ReportsDoughnut from './ReportsDoughnut'
import ReportsChart from './ReportsChart'

export default function Reports({ toSummary }) {
	const { api } = useContext(Context)
	const isLogged = true
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

	const linesNames = {
		python_all: { title: 'Python', color: 'hsl(221, 24%, 32%)' },
		mathcad_report: { title: 'Mathcad', color: '#3D84A8' },
		physical_statement: { title: 'Физика', color: '#46CDCF' },
		mechanics_statement: { title: 'Механика', color: '#ABEDD8' },
		python_percent: { title: 'Python, %', color: 'hsl(221, 24%, 32%)' },
		'python_all+mathcad_report': {
			title: 'Протоколы механика',
			color: '#3D84A8',
		},
	}

	return (
		<>
			{toSummary ? (
				/* ФРАГМЕНТ ДЛЯ ЭКСПОРТА В SUMMARY */
				<React.Fragment>
					<div className="chart-card card-item reports-charts">
						<h1 className="reports__title">Статистика</h1>
						<div className="reports-charts__item">
							<h3>Ведомости и протоколы</h3>
							<div className="chart-card__chart ">
								{reportsLoaded ? (
									<ReportsChart
										dataset={{
											reports: reports.reports,
											dates: reports.dates,
										}}
										reportsKeys={[
											'physical_statement',
											'mechanics_statement',
											'python_all+mathcad_report',
										]}
										linesNames={linesNames}
									/>
								) : (
									<div className="blank-page-ar-2"></div>
								)}
							</div>
						</div>
						<div className="reports-charts__item">
							<h3>Внедрение Python</h3>
							<div className="chart-card__chart ">
								{reportsLoaded ? (
									<ReportsChart
										dataset={{
											reports: reports.reports,
											dates: reports.dates,
										}}
										reportsKeys={['python_percent']}
										linesNames={linesNames}
									/>
								) : (
									<div className="blank-page-ar-2"></div>
								)}
							</div>
						</div>
						<div className="reports-charts__item">
							<h3>Протоклы Python и Mathcad</h3>
							<div className="chart-card__chart ">
								{reportsLoaded ? (
									<ReportsChart
										dataset={{
											reports: reports.reports,
											dates: reports.dates,
										}}
										reportsKeys={['python_all', 'mathcad_report']}
										linesNames={linesNames}
									/>
								) : (
									<div className="blank-page-ar-2"></div>
								)}
							</div>
						</div>
					</div>
				</React.Fragment>
			) : (
				/* ФРАГМЕНТ СТРАНИЦЫ С ОТЧЕТАМИ */
				<React.Fragment>
					{isLogged ? (
						<div className="transparent-item reports-grid chart-card_reports">
							<div className="chart-card card-item reports-charts">
								<h1 className="reports__title">Статистика</h1>
								<div className="reports-charts__item">
									<h3>Ведомости и протоколы</h3>
									<div className="chart-card__chart ">
										{reportsLoaded ? (
											<ReportsChart
												dataset={{
													reports: reports.reports,
													dates: reports.dates,
												}}
												reportsKeys={[
													'physical_statement',
													'mechanics_statement',
													'python_all+mathcad_report',
												]}
												linesNames={linesNames}
											/>
										) : (
											<div className="blank-page-ar-2"></div>
										)}
									</div>
								</div>
								<div className="reports-charts__item">
									<h3>Внедрение Python</h3>
									<div className="chart-card__chart ">
										{reportsLoaded ? (
											<ReportsChart
												dataset={{
													reports: reports.reports,
													dates: reports.dates,
												}}
												reportsKeys={['python_percent']}
												linesNames={linesNames}
											/>
										) : (
											<div className="blank-page-ar-2"></div>
										)}
									</div>
								</div>
								<div className="reports-charts__item">
									<h3>Протоклы Python и Mathcad</h3>
									<div className="chart-card__chart ">
										{reportsLoaded ? (
											<ReportsChart
												dataset={{
													reports: reports.reports,
													dates: reports.dates,
												}}
												reportsKeys={['python_all', 'mathcad_report']}
												linesNames={linesNames}
											/>
										) : (
											<div className="blank-page-ar-2"></div>
										)}
									</div>
								</div>
							</div>
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
							<div className="chart-card card-item reports__doughnut-item">
								<h1 className="reports__title">Протоколы на Python</h1>
								<div className="reports__doughnut">
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
						</div>
					) : (
						<NotLogged />
					)}
				</React.Fragment>
			)}
		</>
	)
}
