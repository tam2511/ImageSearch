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
			<figcaption>Score: ${imageItem.score.toFixed(2)}</figcaption>
		</figure>
	`
}

const uploadFileOnServer = async () => {
	let response = undefined
	const fileInput = document.querySelector(
		SELECTORS.formZipInput
	) as HTMLInputElement
	const uploadButton = document.querySelector(SELECTORS.buttonUploadZip)

	const zipFile = fileInput && fileInput.files && fileInput.files[0]

	const formData = new FormData()

	if (!fileInput || !zipFile) return

	if (uploadButton) uploadButton.classList.add('is-loading')

	formData.set('zip_file', zipFile)

	try {
		response = await API.doUploadRequest('upload_zip', formData)
	} catch (e) {
		console.error('uploadFileOnServer, e:',e)
	} finally {
		if (uploadButton) uploadButton.classList.remove('is-loading')
	}

	return response
}

const getImages = async (offset: number) => {
	let response = undefined

	const imageInput = document.querySelector(
		SELECTORS.formImageInput
	) as HTMLInputElement
	const uploadButton = document.querySelector(SELECTORS.buttonInitialSearch)


	const file = imageInput && imageInput.files && imageInput.files[0]
	const formData = new FormData()

	if (!imageInput || !file) return

	if (uploadButton) uploadButton.classList.add('is-loading')

	formData.set('image', file)
	try {
		response = await API.doUploadRequest('search', formData, `/?limit=50&offset=${offset}`)
	} catch (e) {
		console.error('getImages, e:',e)
	} finally {
		if (uploadButton) uploadButton.classList.remove('is-loading')
	}

	return response
}

const renderImages = (images: ImageSearchResponse) => {
	const { items, limit } = images

	const gallery = document.querySelector(SELECTORS.galleryImages)

	if (!gallery) return

	if (!items.length) {
		gallery.classList.remove(CLASSES.galleryImagesActive)
	} else if (items.length === limit ){
		gallery.classList.add(CLASSES.galleryImagesActive)
	}

	for (let i = 0; i < items.length; i++) {
		const imageElement = createImage(items[i])

		gallery.insertAdjacentHTML('beforeend', imageElement)
	}

}

const setPreviewAndLabel = () => {
	const inputImage = document.querySelector(SELECTORS.formImageInput)
	const labelImage = document.querySelector(SELECTORS.formImageLabel)
	const inputZip = document.querySelector(SELECTORS.formZipInput)
	const labelZip = document.querySelector(SELECTORS.formZipLabel)
	const userPreview = document.querySelector(SELECTORS.userFilePreview)

	const inputs = [{
		input: inputImage,
		label: labelImage,
		preview: userPreview as HTMLImageElement
	}, {
		input: inputZip,
		label: labelZip
	}]

	inputs.forEach((item) => {
		if (item.input && item.label) {
			item.input.addEventListener('input', (e) => {
				const target = e.target as HTMLInputElement
				if (target.files && target.files[0]) {
					if (item.label) item.label.textContent = target.files[0].name

					if (item.preview) item.preview.src = URL.createObjectURL(target.files[0])
				}
			})
		}
	})
}

export default {
	getImages,
	clearImages,
	createImage,
	renderImages,
	uploadFileOnServer,
	setPreviewAndLabel
}