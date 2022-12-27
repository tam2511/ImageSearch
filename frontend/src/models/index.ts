export interface ImageItem {
	id: string
	score: number
	image_path: string
}

export interface ImageSearchResponse {
	items: ImageItem[]
	limit: number
	offset: number
	total: number
}
export type Actions = 'search' | 'faq' | 'upload' | 'pagination' | 'initial-search' | 'upload-zip'
