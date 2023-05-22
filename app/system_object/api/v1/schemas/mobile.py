from pydantic import BaseModel, Field

from system.config import settings


class MobileVersionsResponse(BaseModel):
    current_version: int = \
        Field(...,
              title='current_version',
              description='current mobile version',
              example=5,
              )
    min_version: int = \
        Field(...,
              title='min_version',
              description='minimum mobile version',
              example=3,
              )
    current_version_name: str = \
        Field(...,
              title='current_version_name',
              description='current mobile version name',
              example="1.0.5",
              )
    min_version_name: str = \
        Field(...,
              title='min_version_name',
              description='minimum mobile version name',
              example="0.9.4",
              )

    force_update_display_message: str = \
        Field(...,
              title='force_update_display_message',
              description='message show on force update proccess',
              example="version ghabli rahmata geddi. update kon balam jaan!",
              )

    download_link_play_store: str = \
        Field(...,
              title='download_link_play_store',
              description='application link on play store',
              example="https://www.google.com",
              )

    download_link_play_bazaar: str = \
        Field(...,
              title='download_link_play_store',
              description='application link on play bazaar',
              example="https://www.google.com",
              )

    force_update_display_myket: str = \
        Field(...,
              title='force_update_display_myket',
              description='application link on Myket',
              example="https://www.google.com",
              )

    api_base_url: str = \
        Field(...,
              title='api_base_url',
              description='backend application base url',
              example=settings.WALLPAY_BASE_URL,
              )

    maintenance_mode: bool = \
        Field(...,
              title='maintenance_mode',
              description='is app in maintain or not',
              example=False,
              )

    maintenance_mode_message: str = \
        Field(...,
              title='maintenance_mode_message',
              description='message showed when maintain mode is true',
              example="app be chokh rafte, badan bia dobare",
              )

    estimated_time_to_availability: int = \
        Field(...,
              title='estimated_time_to_availability',
              description='estimated time that app will be available in second',
              example=1000,
              )
