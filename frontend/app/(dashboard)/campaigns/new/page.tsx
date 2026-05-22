import { redirect } from 'next/navigation'

// Campaign creation has moved to a multi-step modal on /campaigns
export default function NewCampaignRedirect() {
  redirect('/campaigns')
}
