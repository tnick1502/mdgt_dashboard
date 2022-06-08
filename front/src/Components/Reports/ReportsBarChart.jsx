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
	BarElement,
} from 'chart.js'
import { Bar } from 'react-chartjs-2'

ChartJS.register(
	CategoryScale,
	LinearScale,
	PointElement,
	LineElement,
	BarElement,
	Title,
	Tooltip,
	Legend
)

export default function ReportsBarChart({ dataset }) {
	const inputData = { ...dataset.reports }

	const reportsDatasets = []
	const labels = []

	const labelsNames = {
		python_all: 'Питон',
		mathcad_report: 'Маткад',
		physical_statement: 'Физика',
		mechanics_statement: 'Механика',
	}

	const types = Object.keys(labelsNames)
	types.forEach((type) => {
		reportsDatasets.push(inputData[type])
		labels.push(labelsNames[type])
	})

	const typesColors = ['hsl(221, 24%, 32%)', '#3D84A8', '#46CDCF', '#ABEDD8']

	function colorize() {
		return (ctx) => {
			const type = ctx.parsed.x
			const c = typesColors[type]

			return c
		}
	}

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
					text: 'Число протоколов',
					font: {
						size: 16,
					},
					color: 'black',
					align: 'center',
				},
				suggestedMin: 0,
				suggestedMax: Math.max(...reportsDatasets),
				ticks: {
					color: 'black',
					font: {
						size: 16,
					},
				},
			},
		},
		elements: {
			bar: {
				backgroundColor: colorize(),
				borderColor: colorize(),
				borderWidth: 0,
				borderRadius: 5,
				borderSkipped: true,
			},
		},
	}

	const data = {
		labels,
		datasets: [
			{
				label: 'Количество',
				data: reportsDatasets,
			},
		],
	}

	return (
		<React.Fragment>
			<Bar options={options} data={data} />
		</React.Fragment>
	)
}
