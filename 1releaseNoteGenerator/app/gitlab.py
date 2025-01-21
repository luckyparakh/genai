from dotenv import load_dotenv
from fastapi import HTTPException
import httpx
from model import GitLabTagResponse, UserInput, GitLabCommitsResponse, Commit
import logging
load_dotenv()


async def get_data(input_data: UserInput, logger: logging.Logger):
    latest_tag_details = await get_latest_tag_details(input_data, logger)
    return await get_delta_commits(input_data, latest_tag_details.commit.created_at, logger)


async def get_latest_tag_details(input: UserInput, logger: logging.Logger) -> GitLabTagResponse:
    logger.info("Get Latest Tag")
    headersList = {
        "PRIVATE-TOKEN": input.access_token
    }
    tags_endpoint = f"https://{input.base_url}/api/v4/projects/{input.project_id}/repository/tags"
    logger.debug(f"Latest Tag URL: {tags_endpoint}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(tags_endpoint, headers=headersList, params={"sort": "desc", "per_page": 1})
            response.raise_for_status()  # Raises httpx.HTTPStatusError for non-200 status
            tags = response.json()
            logger.debug(f"Response: {tags}")
            if not tags:
                raise HTTPException(
                    status_code=404, detail="No tags found for the given project.")
            # Parse the latest tag using Pydantic
            latest_tag = GitLabTagResponse(**tags[0])
            logger.debug(f"Latest Tag JSON: {latest_tag}")
            return latest_tag

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Request error: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error: {str(e)}")


async def get_delta_commits(input, last_commit_created_at, logger) -> str:
    logger.info("Get Delta Commits")
    headersList = {
        "PRIVATE-TOKEN": input.access_token
    }
    reference_branch = "develop"
    commits_endpoint = f"https://{input.base_url}/api/v4/projects/{input.project_id}/repository/commits"
    logger.debug(f"Delta Commit URL: {commits_endpoint}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(commits_endpoint, headers=headersList,
                                        params={"ref_name": reference_branch, "since": last_commit_created_at})
            response.raise_for_status()  # Raises httpx.HTTPStatusError for non-200 status
            output = response.json()
            logger.debug(f"Response: {output}")
            if not output:
                raise HTTPException(
                    status_code=404, detail="No commits found.")
            titles = []
            for commit in output:
                # Parse the commits using Pydantic
                c = Commit(**commit)
                titles.append(c.title)
            joinedTitles= "\n\n".join(titles)
            logger.debug(f"Response: {joinedTitles}")
            return joinedTitles

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Request error: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error: {str(e)}")
