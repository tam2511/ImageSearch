import { ImageItem } from '../models'
// import MockData from './mockData'

const API_URL = '/api'

// const min = () => Math.floor(Math.random() * 1000000)
//
// const generateTestData = (images: string[]) => {
// 	const result = []
//
// 	for (let i = 0; i < images.length; i++) {
// 		result.push({
// 			score: `0.${Math.round(min() + Math.random() * 100000)}`,
// 			id: Math.random() * 10,
// 			image: images[i]
// 		})
// 	}
//
// 	return result
// }

// const testData: ImageItem[] = generateTestData(
// 	MockData.testImages2
// ) as unknown as ImageItem[]

// const doPostRequest = async (api: string, body: unknown) => {
// 	const response = await fetch(`${API_URL}/${api}`, {
// 		method: 'POST', // *GET, POST, PUT, DELETE, etc.
// 		credentials: 'same-origin', // include, *same-origin, omit
// 		headers: {
// 			'Content-Type': 'application/json'
// 			// 'Content-Type': 'application/x-www-form-urlencoded',
// 		},
// 		redirect: 'follow', // manual, *follow, error
// 		referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
// 		body: JSON.stringify(body) // body data type must match "Content-Type" header
// 	})
// 	return response.json() // parses JSON response into native JavaScript objects
// }

const doUploadRequest = async (
	api: string,
	formData: BodyInit | null | undefined,
	offset: number
): Promise<ImageItem[] | undefined> => {
	try {
		const response = await fetch(`${API_URL}/${api}/?limit=50&offset=${offset}`, {
			method: 'POST',
			headers: {
				Accept: 'application/json'
			},
			body: formData
		})

		return await response.json()
	} catch (e) {
		console.error('doPutRequest, error: ', e)
		return undefined
	}
}
//
// const getTestImages = async (url: string, data: unknown) => {
// 	console.debug(url, data)
// 	return await new Promise((resolve) => {
// 		setTimeout(() => {
// 			resolve(testData)
// 			return testData
// 		}, 2000)
// 	})
// }

export default {
	doUploadRequest
	// getTestImages
}
