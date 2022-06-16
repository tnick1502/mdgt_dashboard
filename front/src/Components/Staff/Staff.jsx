import React, { useEffect, useState, useContext } from 'react'
import { useRef } from 'react'
import Context from '../../context'

import './Staff.css'

export default function Staff() {
	const { isLogged, api } = useContext(Context)
	const [birthdays, setBirthdays] = useState([])
	const [loaded, setLoaded] = useState(false)
	const [isHided, setIsHided] = useState('hided')
	const [currentBD, setCurrentBD] = useState(0)

	const currentMonth = useRef(new Date().getMonth() + 1)
	// const currentMonth = useRef(5)

	useEffect(() => {
		if (!isLogged) {
			setLoaded(false)
			setBirthdays([])
			return
		}

		function updateStaff() {
			if (isLogged) {
				fetch(`${api}staff/month_birthday/?month=${currentMonth.current}`)
					.then((response) => response.json())
					.then((data) => {
						if (
							data &&
							data.length > 0 &&
							'birthday' in data[0] &&
							data[0].birthday.split('-').length === 3
						) {
							setBirthdays(data)
							setLoaded(true)
						}
					})
			}
		}

		updateStaff()

		const interval = setInterval(updateStaff, 100000)

		return () => {
			clearInterval(interval)
		}
	}, [isLogged])

	useEffect(() => {
		function hide(current) {
			setIsHided('hided')
			setTimeout(() => {
				setIsHided('')
				setCurrentBD(current)
			}, 2000)
		}

		setIsHided('')
		if (birthdays.length < 1) return

		let current = 1
		const birthdayUpdate = setInterval(() => {
			hide(current)
			if (current < birthdays.length - 1) {
				current = current + 1
			} else {
				current = 0
			}
		}, 6000)

		return () => {
			clearInterval(birthdayUpdate)
		}
	}, [birthdays])

	return (
		<>
			<div className="staff-item card-item">
				<h3>Дни рождения в этом месяце: </h3>
				<div
					className={`staff__name ${isHided} ${
						loaded &&
						birthdays[currentBD].birthday.split('-')[2].replace('0', '') ===
							new Date().getDate().toString()
							? 'current'
							: ''
					}`}
				>
					{loaded
						? `${birthdays[currentBD].birthday.split('-')[2]} - ${
								birthdays[currentBD].full_name
						  }`
						: 'Отсутствуют'}
				</div>
			</div>
		</>
	)
}
