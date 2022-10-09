import './style.scss'
import API from './api'
import { ImageItem } from './models'

type Actions = 'search' | 'faq' | 'upload'

let isLoading = false

const createImage = (imageItem: ImageItem) => {
	const prefix = 'data:image/jpeg;base64,'

	return `
		<figure>
			<img src="${prefix + imageItem.image}"
					 alt="${imageItem.id}">
			<figcaption>Score: ${imageItem.score}</figcaption>
		</figure>
	`
}

const getImages = async () => {
	console.log('getImages')
	const image = document.querySelector('form input') as HTMLInputElement

	const file = image && image.files && image.files[0]
	const formData = new FormData()

	if (!image || !file) return

	formData.set('image', file)

	return await API.getTestImages('search?number_images=10', formData)
}
const renderImages = (images: ImageItem[]) => {
	console.log('renderImages, images: ', images)
	const gallery = document.querySelector('.gallery')
	if (!gallery) return

	for (let i = 0; i < images.length; i++) {
		const imageElement = createImage(images[i])

		gallery.insertAdjacentHTML('beforeend', imageElement)
	}
}

const doActions = async (action: Actions) => {
	console.log('doActions, action: ', action)
	switch (action) {
		case 'search':
			isLoading = true

			const images = (await getImages()) as unknown as ImageItem[]

			console.log('doActions, images: ', images)

			isLoading = false

			if (!images) return

			renderImages(images)
	}
}

document.addEventListener('click', async ({ target }) => {
	const action = (target as HTMLButtonElement)?.dataset.action as Actions

	if (!action) return

	await doActions(action)
})
