import React from 'react'
import {
	Chart as ChartJS,
	CategoryScale,
	LinearScale,
	PointElement,
	LineElement,
	Title,
	Tooltip,
	Legend,
} from 'chart.js'
import { Line } from 'react-chartjs-2'

ChartJS.register(
	CategoryScale,
	LinearScale,
	PointElement,
	LineElement,
	Title,
	Tooltip,
	Legend
)

export default function ReportsChart({ dataset, reportsKeys, linesNames }) {
	const inputData = { reports: [...dataset.reports], dates: [...dataset.dates] }

	const dates = [...inputData.dates]

	let prevYear = parseFloat(dates[0].split(' ')[1])
	dates[0] = dates[0].split(' ')
	for (let i = 1; i < dates.length; i++) {
		const currentDate = dates[i].split(' ')

		if (parseFloat(currentDate[1]) > prevYear) {
			prevYear = parseFloat(currentDate[1])
			dates[i] = [currentDate[0].slice(0, 3), currentDate[1]]
		} else {
			dates[i] = currentDate[0].slice(0, 3)
		}
	}
	inputData.dates = dates
	const labels = inputData.dates

	const reportsDatasets = []

	// const types = Object.keys(linesNames)
	const types = reportsKeys
	types.forEach((type) => {
		const lineData = []

		for (let i = 0; i < inputData.reports.length; i++) {
			const joinTypes = type.split('+')
			let sum = 0
			joinTypes.forEach((jointype) => {
				sum += inputData.reports[i][jointype.replace(/\s+/g, '')]
			})
			lineData.push(sum)
		}

		reportsDatasets.push({
			label: linesNames[type].title,
			data: lineData,
			borderColor: linesNames[type].color,
			backgroundColor: linesNames[type].color,
			fill: false,
			cubicInterpolationMode: 'monotone',
			tension: 0.4,
		})
	})

	const options = {
		responsive: true,
		maintainAspectRatio: false,
		plugins: {
			title: {
				display: false,
				text: 'Chart.js Line Chart - Cubic interpolation mode',
			},
			legend: {
				display: true,
				position: 'bottom',
			},
		},
		interaction: {
			intersect: false,
		},
		scales: {
			x: {
				display: true,
				title: {
					display: false,
				},
				ticks: {
					color: 'black',
					font: {
						size: 16,
					},
				},
			},
			y: {
				display: true,
				title: {
					display: false,
					text: 'Количество',
					font: {
						size: 16,
					},
					color: 'black',
					align: 'center',
				},
				suggestedMax: 100,
				suggestedMin: 0,
				ticks: {
					color: 'black',
					font: {
						size: 16,
					},
				},
			},
		},
	}

	const data = {
		labels,
		datasets: reportsDatasets,
	}

	return (
		<React.Fragment>
			<Line options={options} data={data} />
		</React.Fragment>
	)
}
