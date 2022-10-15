import './style.scss'
import Helpers from './helpers'
import { Actions } from './models'
import { CONSTANTS } from './constanst'

const state = {
	isLoading: false,
	offset: 0
}

const uploadZip = async () => {
	state.isLoading = true

	await Helpers.uploadFileOnServer()

	state.isLoading = false
}

const initialSearch = async () => {
	Helpers.clearImages()
	state.offset = 0
	await doActions('search')
}

const search = async () => {
	state.isLoading = true

	const images = await Helpers.getImages(state.offset)

	state.isLoading = false

	if (!images) return

	Helpers.renderImages(images)
}

const pagination = async () => {
	state.offset += CONSTANTS.additionalOffset
	await doActions('search')
}

const doActions = async (action: Actions) => {
	switch (action) {
		case 'initial-search':
			await initialSearch()
			break
		case 'search':
			await search()
			break
		case 'pagination':
			await pagination()
			break
		case 'upload-zip':
			await uploadZip()
			break
	}
}


const init = async () => {
	Helpers.setPreviewAndLabel()

	document.addEventListener('click', async ({ target }) => {
		const action = (target as HTMLButtonElement)?.dataset.action as Actions

		if (!action) return

		await doActions(action)
	})
}

init()
