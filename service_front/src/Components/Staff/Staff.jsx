import React, { useEffect, useState, useContext } from 'react'
import { useRef } from 'react'
import Context from '../../context'

import './Staff.css'

export default function Staff() {
	const { isLogged, api } = useContext(Context)
	const [birthdays, setBirthdays] = useState([])
	const [loaded, setLoaded] = useState(false)

	const currentMonth = useRef(new Date().getMonth() + 1)

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

	function formDay(day) {
		const options = { day: 'numeric', month: 'long' }
		const date = new Intl.DateTimeFormat('ru-RU', options).format(new Date(day))
		return date
	}

	function fromName(fullname) {
		const splitName = fullname.split(' ')
		if (splitName.length < 3) {
			return fullname
		}

		return (
			<>
				{`${splitName[1]} ${splitName[2]}`}
				<div className="bd-card__name_sub">{splitName[0]}</div>
			</>
		)
	}

	return (
		<>
			<div className="staff-item card-item">
				<h1>Дни рождения в этом месяце</h1>
				<div className="bd-grid">
					{loaded
						? birthdays.map((bd) => (
								<div className="bd-card" key={bd.phone}>
									<div className="bd-card__name">{fromName(bd.full_name)}</div>
									<div className="bd-card__phone">
										<svg
											xmlns="http://www.w3.org/2000/svg"
											width="24"
											height="24"
										>
											<path d="m20.487 17.14-4.065-3.696a1.001 1.001 0 0 0-1.391.043l-2.393 2.461c-.576-.11-1.734-.471-2.926-1.66-1.192-1.193-1.553-2.354-1.66-2.926l2.459-2.394a1 1 0 0 0 .043-1.391L6.859 3.513a1 1 0 0 0-1.391-.087l-2.17 1.861a1 1 0 0 0-.29.649c-.015.25-.301 6.172 4.291 10.766C11.305 20.707 16.323 21 17.705 21c.202 0 .326-.006.359-.008a.992.992 0 0 0 .648-.291l1.86-2.171a.997.997 0 0 0-.085-1.39z"></path>
										</svg>
										<div className="bd-card__phone_phone">
											{`+${bd.phone}`}
											<div className="bd-card__phone_sub">Мобильный</div>
										</div>
									</div>
									<div className="bd-card__day">
										<svg
											xmlns="http://www.w3.org/2000/svg"
											width="24"
											height="24"
										>
											<path d="M7 11h2v2H7zm0 4h2v2H7zm4-4h2v2h-2zm0 4h2v2h-2zm4-4h2v2h-2zm0 4h2v2h-2z"></path>
											<path d="M5 22h14c1.103 0 2-.897 2-2V6c0-1.103-.897-2-2-2h-2V2h-2v2H9V2H7v2H5c-1.103 0-2 .897-2 2v14c0 1.103.897 2 2 2zM19 8l.001 12H5V8h14z"></path>
										</svg>
										{formDay(bd.birthday)}
									</div>
								</div>
						  ))
						: null}
				</div>
			</div>
		</>
	)
}
