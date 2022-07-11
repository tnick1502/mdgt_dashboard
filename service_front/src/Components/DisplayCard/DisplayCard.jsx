import React from 'react'
import PropTypes from 'prop-types'

import Context from '../../context'
import './DisplayCard.css'
import { useState, useContext } from 'react'

function DisplayCard({
	title,
	prize,
	date,
	chartLoaded,
	type,
	unit,
	closeBtn,
	id,
	divInfo,
}) {
	const [isHided, setIsHided] = useState(false)
	const { hidedCards, setHidedCards } = useContext(Context)

	function onCloseBtn() {
		setHidedCards(() => {
			hidedCards[id] = true
			return hidedCards
		})
		if (id in hidedCards) {
			setIsHided(true)
		}
	}

	const colors = { good: 'good', bad: 'bad', neutral: '' }
	let colorClass = ''

	if (!date) {
		date = ' '
	}

	if (Object.keys(colors).includes(type)) {
		colorClass = colors[type]
	}

	return (
		<>
			{id in hidedCards || isHided ? null : (
				<div className="current-prize card-item">
					{title ? <div className="current-prize__title">{title}</div> : null}
					<div className={'current-prize__prize ' + colorClass}>
						{chartLoaded ? (
							<>
								{Math.trunc(prize)}
								{Math.round((prize % 1) * 100, -2) === 0 ? null : (
									<p id="not-int-unit-part">
										.{Math.round((prize % 1) * 100, -2)}
									</p>
								)}
								<p>{unit ? unit : ''}</p>
							</>
						) : null}
					</div>
					<div className="current-prize__sub">
						<div className="current-prize__date">{date}</div>
						<div
							className={divInfo ? 'current-prize__growth ' + divInfo.key : ''}
						>
							{divInfo ? (
								<>
									{divInfo.key === 'good' ? (
										<svg
											xmlns="http://www.w3.org/2000/svg"
											width="24"
											height="24"
										>
											<path d="m6.293 13.293 1.414 1.414L12 10.414l4.293 4.293 1.414-1.414L12 7.586z"></path>
										</svg>
									) : (
										<svg
											xmlns="http://www.w3.org/2000/svg"
											width="24"
											height="24"
										>
											<path d="M16.293 9.293 12 13.586 7.707 9.293l-1.414 1.414L12 16.414l5.707-5.707z"></path>
										</svg>
									)}
									{divInfo.value}%
								</>
							) : null}
						</div>
					</div>

					{closeBtn ? (
						<button onClick={onCloseBtn} className="current-prize__close-btn">
							<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24">
								<path d="m16.192 6.344-4.243 4.242-4.242-4.242-1.414 1.414L10.535 12l-4.242 4.242 1.414 1.414 4.242-4.242 4.243 4.242 1.414-1.414L13.364 12l4.242-4.242z"></path>
							</svg>
						</button>
					) : null}
				</div>
			)}
		</>
	)
}

DisplayCard.propTypes = {
	title: PropTypes.string,
	prize: PropTypes.number,
	date: PropTypes.string,
	chartLoaded: PropTypes.bool.isRequired,
	type: PropTypes.string,
	unit: PropTypes.string,
	closeBtn: PropTypes.bool,
	divInfo: PropTypes.object,
}

export default DisplayCard
