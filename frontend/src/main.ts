import './style.scss'
import API from './api'
import { ImageItem } from './models'

type Actions = 'search' | 'faq' | 'upload' | 'pagination'

const SELECTORS = {
	galleryImages: '.gallery-images',
	formInput: '.search input[type="file"]',
	userFilePreview: '.user-file_preview'
}

// let isLoading = false
const state = {
	isLoading: false,
	offset: 0
}

const createImage = (imageItem: ImageItem) => {
	// const prefix = 'data:image/jpeg;base64,'
	// const src = prefix + imageItem.image

	return `
		<figure>
			<img src="${imageItem.image}"
					 alt="${imageItem.id}">
			<figcaption>Score: ${imageItem.score}</figcaption>
		</figure>
	`
}

const getImages = async () => {
	const image = document.querySelector(
		SELECTORS.formInput
	) as HTMLInputElement

	const file = image && image.files && image.files[0]
	const formData = new FormData()

	if (!image || !file) return

	formData.set('image', file)

	return await API.doUploadRequest('search?number_images=10', formData)
}
const renderImages = (images: ImageItem[]) => {
	const gallery = document.querySelector(SELECTORS.galleryImages)

	if (!gallery) return

	for (let i = 0; i < images.length; i++) {
		const imageElement = createImage(images[i])

		gallery.insertAdjacentHTML('beforeend', imageElement)
	}

	gallery.classList.add('gallery-images_active')
}

const doActions = async (action: Actions) => {
	switch (action) {
		case 'search':
			state.isLoading = true

			const images = (await getImages()) as unknown as ImageItem[]

			state.isLoading = false

			if (!images) return

			renderImages(images)
			break
		case 'pagination':
			state.offset += 10
			await doActions('search')
	}
}

document.addEventListener('click', async ({ target }) => {
	const action = (target as HTMLButtonElement)?.dataset.action as Actions

	if (!action) return

	await doActions(action)
})

const init = async () => {
	const input = document.querySelector(SELECTORS.formInput)

	if (input) {
		input.addEventListener('input', (e) => {
			const target = e.target as HTMLInputElement
			if (target.files && target.files[0]) {
				const userPreviewFile = document.querySelector(
					SELECTORS.userFilePreview
				) as HTMLImageElement

				if (!userPreviewFile) return

				userPreviewFile.src = URL.createObjectURL(target.files[0])
			}
		})
	}
}

init()
