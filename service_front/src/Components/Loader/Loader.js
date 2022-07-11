import React from 'react'
import './Loader.css'

export default function Loader() {
	return (
		<React.Fragment>
			<div
				style={{
					display: 'flex',
					justifyContent: 'center',
					margin: '0',
					transform: 'scale(0.5)',
					WebkitTransform: 'scale(0.5)',
					transformOrigin: 'top center',
				}}
			>
				<div className="lds-spinner">
					<div />
					<div />
					<div />
					<div />
					<div />
					<div />
					<div />
					<div />
					<div />
					<div />
					<div />
					<div />
				</div>
			</div>
		</React.Fragment>
	)
}
