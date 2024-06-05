import { Link } from 'react-router-dom'
import { replaceUrl } from '../../../helpers/replaceUrl'
import { ProductType } from '../../../types/ProductType'
import Tag from '../Tag'

export default function SubscriptionCard({ subscription }: { subscription: ProductType }) {
    return (
        <Link to={`/subscription/${subscription?.id}/${subscription?.publications[0]?.id}`} className='w-full h-full flex flex-col items-start justify-between'>
            <img className='rounded-xl max-h-[200px] mb-[18px]' src={replaceUrl(subscription?.publications[0]?.offer_image)} alt="subscription image" />
            <h1 className='text-title text-start'>{subscription?.title}</h1>
            {subscription?.publications && <h2 className='text-subtitle'>{subscription?.publications[0]?.title}</h2>}
            <div className='flex gap-2'>
                <h3 className='price-small'>
                    {subscription?.publications[0]?.final_price} ₽
                </h3>
                {subscription?.publications[0] && subscription?.publications[0]?.discount !== 0 && <Tag type="discount">-{subscription?.publications[0]?.discount}%</Tag>}
            </div>
        </Link>
    )
}
