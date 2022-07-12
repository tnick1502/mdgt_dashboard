export function parsePrizes(data) {
	const options = { year: 'numeric', month: 'short' }

	const prizes = []
	const dates = []

	const items = Object.keys(data)

	let lastDate = null

	if (items.length > 0) {
		items.forEach((item) => {
			prizes.push(data[item].prize)
			lastDate = new Date(data[item].date)
			const date = new Intl.DateTimeFormat('ru-RU', options)
				.format(new Date(data[item].date))
				.replace(' г.', '')

			dates.push(date)
		})
	}
	const currentDate = new Date()
	if (currentDate.getMonth() > lastDate.getMonth()) {
		prizes.push(0)
		dates.push(
			new Intl.DateTimeFormat('ru-RU', options)
				.format(currentDate)
				.replace(' г.', '')
		)
	}

	const resultData = { prizes: prizes, dates: dates }
	return resultData
}

export async function getPrizes() {
	const range = 300
	return {
		prizes: [
			Math.round(Math.random() * range),
			Math.round(Math.random() * range),
			Math.round(Math.random() * range),
			Math.round(Math.random() * range),
			Math.round(Math.random() * range),
			Math.round(Math.random() * range),
			Math.round(Math.random() * range),
		],
		dates: ['янв', 'февр', 'мар', 'апр', 'май', 'июнь', 'июль'],
	}
}

export async function login(username, password) {
	if (username === 'test' && password === '911') {
		return true
	}
	return false
}

export function parseReports(data) {
	const options = { year: 'numeric', month: 'short' }

	const reports = []
	const dates = []

	const items = Object.keys(data)

	if (items.length > 0) {
		items.forEach((item) => {
			const reportItem = { ...data[item] }
			delete reportItem.date
			reports.push(reportItem)
			const date = new Intl.DateTimeFormat('ru-RU', options)
				.format(new Date(data[item].date))
				.replace(' г.', '')

			dates.push(date)
		})
	}

	const resultData = { reports: reports, dates: dates }

	return resultData
}

export function parsePayments(data) {
	const options = { year: 'numeric', month: 'short' }

	if (data.length < 1) {
		return { payments: null, dates: null, summ: null }
	}
	const payments = {}
	const dates = []

	// Сначала заполняем всех людей какие вообще могут быть в данных
	for (let i = 0; i < data.length; i++) {
		const keys = Object.keys(data[i])
		keys
			.filter((v) => v !== 'data')
			.forEach((key) => {
				if (!(key in payments)) {
					payments[key] = []
				}
			})
	}

	const summ = []
	const keys = Object.keys(payments)
	// Проходим по всем датам
	for (let i = 0; i < data.length; i++) {
		// Для каждого ключа у нас или есть значение или его нет
		// Необходимо для того, что если позднее появится новый ключ
		//  которого нет в предыдущих данных все не упало
		keys.forEach((key) => {
			if (key in data[i]) {
				payments[key].push(data[i][key])
			} else {
				payments[key].push(null)
			}
		})

		// Сумму посчитаем сразу
		let sumVal = 0
		keys.forEach((key) => {
			sumVal = sumVal + payments[key][i]
		})
		summ.push(sumVal)

		// И оформим даты
		const date = new Intl.DateTimeFormat('ru-RU', options)
			.format(new Date(data[i].data))
			.replace(' г.', '')

		dates.push(date)
	}

	const resultData = { payments: payments, dates: dates, summ: summ }

	return resultData
}

export function phoneFormatter(phoneNumber) {
	let formattedNumber = `${phoneNumber}`

	if (formattedNumber.startsWith('8') || formattedNumber.startsWith('7')) {
		formattedNumber = formattedNumber.slice(1, formattedNumber.length)
	}
	return `+7 (${formattedNumber.slice(0, 3)}) ${formattedNumber.slice(
		3,
		6
	)} ${formattedNumber.slice(6, 8)} ${formattedNumber.slice(
		8,
		formattedNumber.length
	)}`
}

export function formDay(day) {
	const options = { day: 'numeric', month: 'long' }
	const date = new Intl.DateTimeFormat('ru-RU', options).format(new Date(day))
	return date
}
