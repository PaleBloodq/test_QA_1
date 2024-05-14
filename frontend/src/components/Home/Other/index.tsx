import { SectionType } from '../../../types/SectionType'
import GamesSlider from '../../common/GamesSlider'
import useIsLoading from '../../../hooks/useIsLoading';

export default function Other({ data }: { data: SectionType[] }) {
    const isLoading = useIsLoading(data[0]?.objects);
    return (
        <div className='flex flex-col'>
            {
                data.map((item, index: number) => {
                    return (
                        <div key={index} className="w-screen relative -ml-[15px]">
                            <div className="max-w-[560px] mx-auto mt-7 pt-6 pb-3 px-0 custom-border flex flex-col">
                                <div className="flex gap-3 items-center mb-4">
                                    <h1 className="text-header ml-5">{item.name}</h1>
                                </div>
                                <div className='ml-2'>
                                    <GamesSlider type={item.objects[0].type} isLoading={isLoading} data={item.objects} />
                                </div>
                            </div>
                        </div>
                    )
                })
            }
        </div>
    )
}
