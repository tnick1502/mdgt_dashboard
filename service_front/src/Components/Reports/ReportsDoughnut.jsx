import React from 'react'
import { Chart as ChartJS, registerables } from 'chart.js'
import { Doughnut } from 'react-chartjs-2'

ChartJS.register(...registerables)

export default function ReportsDoughnut({ dataset }) {
	const inputData = { ...dataset.reports }

	const reportsDatasets = []
	const labels = []

	const labelsNames = {
		python_report: 'Другое',
		python_dynamic_report: 'Динамика',
		python_compression_report: 'Компрессия',
	}

	const types = Object.keys(labelsNames)
	types.forEach((type) => {
		reportsDatasets.push(inputData[type])
		labels.push(labelsNames[type])
	})

	const typesColors = ['#293462', '#F24C4C', '#EC9B3B', '#F7D716']

	const options = {
		responsive: true,
		maintainAspectRatio: false,
		plugins: {
			title: {
				display: false,
				text: 'Соотношение протоколов Python',
			},
			legend: {
				position: 'bottom',
			},
		},
		scales: {
			x: {
				display: false,
			},
			y: {
				display: false,
			},
		},
	}

	const data = {
		labels,
		datasets: [
			{
				label: 'Количество',
				data: reportsDatasets,
				backgroundColor: typesColors,
			},
		],
	}

	return (
		<React.Fragment>
			<Doughnut options={options} data={data} />
		</React.Fragment>
	)
}
