import { NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const session = await getServerSession()
    if (!session) {
      return new NextResponse('Unauthorized', { status: 401 })
    }

    // Call your Django backend API
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/notifications/${params.id}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${session.user.token}`,
      },
    })

    if (!response.ok) {
      throw new Error('Failed to delete notification')
    }

    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('Error deleting notification:', error)
    return new NextResponse('Internal Server Error', { status: 500 })
  }
}
