import { NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'

export async function POST(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const session = await getServerSession()
    if (!session) {
      return new NextResponse('Unauthorized', { status: 401 })
    }

    // Call your Django backend API
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/notifications/${params.id}/read/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${session.user.token}`,
      },
    })

    if (!response.ok) {
      throw new Error('Failed to mark notification as read')
    }

    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('Error marking notification as read:', error)
    return new NextResponse('Internal Server Error', { status: 500 })
  }
}
