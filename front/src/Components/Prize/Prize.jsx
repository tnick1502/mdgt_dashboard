import React, { useContext, useState, useEffect } from 'react'

import './Prize.css'

import Context from '../../context'
import NotLogged from '../NotLogged/NotLogged'
import PrizeChart from './PrizeChart'
import DisplayCard from '../DisplayCard/DisplayCard'
import { parsePrizes } from '../utils'

export default function Prize({ toSummary }) {
	const { isLogged, api } = useContext(Context)
	const [prizes, setPrizes] = useState({ prizes: [], dates: [] })

	const [chartLoaded, setChartLoaded] = useState(false)

	useEffect(() => {
		function updatePrizeChart() {
			if (isLogged) {
				fetch(`${api}prizes/`)
					.then((response) => response.json())
					.then((data) => {
						const resultData = parsePrizes(data)
						setPrizes(resultData)
						setChartLoaded(true)
					})
			}
		}

		updatePrizeChart()

		const interval = setInterval(updatePrizeChart, 100000)

		return () => {
			clearInterval(interval)
		}
	}, [isLogged])

	useEffect(() => {
		if (!isLogged) {
			setPrizes({ prizes: [], dates: [] })
		}
	}, [isLogged])

	function getMean(input) {
		if (input.length > 1) {
			return (
				input.slice(0, -1).reduce((a, b) => a + b) / input.slice(0, -1).length
			)
		}
		return 0
	}

	return (
		<>
			{toSummary ? (
				<React.Fragment>
					<div className="display-cards-wrapper card-item">
						<h1 className="display-cards-wrapper__title unselectable">
							Премия в цифрах
						</h1>
						<div className="display-cards-wrapper__cards">
							<DisplayCard
								title={'Текущая'}
								prize={prizes.prizes[prizes.prizes.length - 1]}
								date={prizes.dates[prizes.prizes.length - 1]}
								chartLoaded={chartLoaded}
								unit={'%'}
								type={
									prizes.prizes[prizes.prizes.length - 1] <
									getMean(prizes.prizes)
										? 'bad'
										: ''
								}
							/>
							<DisplayCard
								title={'Средняя'}
								prize={getMean(prizes.prizes)}
								chartLoaded={chartLoaded}
								unit={'%'}
							/>
							<DisplayCard
								title={'Максимальная'}
								prize={Math.max(...prizes.prizes)}
								date={
									prizes.dates[
										prizes.prizes.indexOf(Math.max(...prizes.prizes))
									]
								}
								chartLoaded={chartLoaded}
								type={'good'}
								unit={'%'}
							/>
						</div>
					</div>
				</React.Fragment>
			) : (
				<React.Fragment>
					{isLogged ? (
						<div className="transparent-item prize-grid unselectable">
							<div className="chart-card card-item">
								<h1 className="chart-card__header">
									Динамика премии в процентах
								</h1>
								<div className="chart-card__chart">
									{chartLoaded ? (
										<PrizeChart dataset={prizes} />
									) : (
										<div className="blank-page-ar-2"></div>
									)}
								</div>
							</div>
							<div className="display-cards-wrapper card-item">
								<h1 className="display-cards-wrapper__title">
									Премия в цифрах
								</h1>
								<div className="display-cards-wrapper__cards">
									<DisplayCard
										title={'Текущая'}
										prize={prizes.prizes[prizes.prizes.length - 1]}
										date={prizes.dates[prizes.prizes.length - 1]}
										chartLoaded={chartLoaded}
										unit={'%'}
										type={
											prizes.prizes[prizes.prizes.length - 1] <
											getMean(prizes.prizes)
												? 'bad'
												: ''
										}
									/>
									<DisplayCard
										title={'Средняя'}
										prize={getMean(prizes.prizes)}
										chartLoaded={chartLoaded}
										unit={'%'}
									/>
									<DisplayCard
										title={'Максимальная'}
										prize={Math.max(...prizes.prizes)}
										date={
											prizes.dates[
												prizes.prizes.indexOf(Math.max(...prizes.prizes))
											]
										}
										chartLoaded={chartLoaded}
										type={'good'}
										unit={'%'}
									/>
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
