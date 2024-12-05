import { NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'

export async function PATCH(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const session = await getServerSession()
    if (!session) {
      return new NextResponse('Unauthorized', { status: 401 })
    }

    const body = await request.json()

    // Call your Django backend API
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/preferences/${params.id}/`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${session.user.token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })

    if (!response.ok) {
      throw new Error('Failed to update preference')
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error updating preference:', error)
    return new NextResponse('Internal Server Error', { status: 500 })
  }
}
