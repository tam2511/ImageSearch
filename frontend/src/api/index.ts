import { ImageSearchResponse } from '../models'

const API_URL = 'http://localhost:11111'

const doUploadRequest = async (
	api: string,
	formData: BodyInit | null | undefined,
	options= ''
): Promise<ImageSearchResponse | undefined> => {
	try {
		const response = await fetch(`${API_URL}/${api}${options}`, {
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

export default {
	doUploadRequest
}
