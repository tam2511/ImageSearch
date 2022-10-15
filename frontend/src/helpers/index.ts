import { ImageItem, ImageSearchResponse } from '../models'
import { CLASSES, SELECTORS } from '../constanst'
import API from '../api'

const clearImages = () => {
	const gallery = document.querySelector(SELECTORS.galleryImages)

	if (!gallery) return

	gallery.innerHTML = ''
}

const createImage = (imageItem: ImageItem) => {
	return `
		<figure>
			<img src="${imageItem.image_path}"
					 alt="${imageItem.id}">
			<figcaption>Score: ${imageItem.score}</figcaption>
		</figure>
	`
}

const uploadFileOnServer = async () => {
	const fileInput = document.querySelector(
		SELECTORS.formZipInput
	) as HTMLInputElement

	const zipFile = fileInput && fileInput.files && fileInput.files[0]
	const formData = new FormData()

	if (!fileInput || !zipFile) return

	formData.set('zip_file', zipFile)

	return await API.doUploadRequest('upload_zip', formData)
}

const getImages = async (offset: number) => {
	const image = document.querySelector(
		SELECTORS.formImageInput
	) as HTMLInputElement

	const file = image && image.files && image.files[0]
	const formData = new FormData()

	if (!image || !file) return

	formData.set('image', file)

	return await API.doUploadRequest('search', formData, `/?limit=50&offset=${offset}`)
}

const renderImages = (images: ImageSearchResponse) => {
	console.log('images: ', images)
	if (!images || (images && !images.total)) {
		console.error('ImageSearch, don\'t have result images')
		return
	}

	const items = images.items

	const gallery = document.querySelector(SELECTORS.galleryImages)

	if (!gallery) return

	for (let i = 0; i < items.length; i++) {
		const imageElement = createImage(items[i])

		gallery.insertAdjacentHTML('beforeend', imageElement)
	}

	gallery.classList.add(CLASSES.galleryImagesActive)
}

export default {
	getImages,
	clearImages,
	createImage,
	renderImages,
	uploadFileOnServer
}