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

export default function prizeChart({ dataset }) {
	const inputData = { prizes: [...dataset.prizes], dates: [...dataset.dates] }

	const options = {
		responsive: true,
		maintainAspectRatio: false,
		plugins: {
			title: {
				display: false,
				text: 'Chart.js Line Chart - Cubic interpolation mode',
			},
			legend: {
				display: false,
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
					text: 'Премия, %',
					font: {
						size: 16,
					},
					color: 'black',
					align: 'center',
				},
				suggestedMin: 0,
				suggestedMax: Math.max(...inputData.prizes),
				ticks: {
					color: 'black',
					font: {
						size: 16,
					},
				},
			},
		},
	}

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

	const data = {
		labels,
		datasets: [
			{
				label: 'Премия',
				data: inputData.prizes,
				borderColor: 'hsl(221, 24%, 32%)',
				fill: false,
				cubicInterpolationMode: 'monotone',
				tension: 0.4,
			},
		],
	}

	return (
		<React.Fragment>
			<Line options={options} data={data} />
		</React.Fragment>
	)
}
