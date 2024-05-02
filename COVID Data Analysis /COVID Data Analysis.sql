--select * from [dbo].[CovidDeaths] order by 3, 4

--select * from [dbo].[CovidVaccinations]

--Select Data that we are going to be using

SELECT LOCATION, DATE, TOTAL_CASES, TOTAL_DEATHS, new_deaths, total_deaths, POPULATION
FROM CovidDeaths
ORDER BY 1,2

--Looking at Total Cases vs Total Deaths
--Shows likelihood of dying if you contract covid in your country
SELECT LOCATION, DATE, TOTAL_CASES, TOTAL_DEATHS, (total_deaths/total_cases) * 100 DEATHPERCENTAGE
FROM CovidDeaths
WHERE LOCATION LIKE '%states%'
ORDER BY 1,2


--Looking at Total Cases vs Population
--Shows what percentage of population got Covid

SELECT LOCATION, DATE, TOTAL_CASES, population, (total_cases/population) * 100 PercentPopulationInfected
FROM CovidDeaths
WHERE LOCATION LIKE '%states%'
ORDER BY 1,2


--Highest Rate by country

SELECT LOCATION,MAX(TOTAL_CASES) AS HighestInfectionCount,  MAX((TOTAL_cases/POPULATION)) * 100 PercentPopulationInfected
FROM CovidDeaths
--WHERE LOCATION LIKE '%states%'
group by location, population
ORDER BY PercentPopulationInfected desc


--Showing Countries with Highest Death Count per population

SELECT LOCATION,MAX(cast(TOTAL_deaths as int)) AS TotalDeath
FROM CovidDeaths
--WHERE LOCATION LIKE '%states%'
WHERE continent is not null
group by location
ORDER BY TotalDeath desc


-- LET'S BREAK THINGS DOWN BY CONTINENT

--SELECT LOCATION, MAX(cast(TOTAL_deaths as int)) AS TotalDeath --CORRECT ONE
--FROM CovidDeaths
--WHERE LOCATION LIKE '%states%'
--WHERE continent is null
--group by LOCATION
--ORDER BY TotalDeath desc

SELECT	continent,MAX(cast(TOTAL_deaths as int)) AS TotalDeath
FROM CovidDeaths
--WHERE LOCATION LIKE '%states%'
WHERE continent is not null
group by continent
ORDER BY TotalDeath desc


--GlOBAL NUMBERS

SELECT date,SUM(new_cases) as total_cases, SUM(cast(new_deaths as int)) as total_deaths, SUM(cast(new_deaths as int))/SUM(New_cases)*100 as DeathPercentage
FROM CovidDeaths
--WHERE LOCATION LIKE '%states%'
where continent is not null
group by date
ORDER BY 1,2


-- Looking at Total Population vs Vaccination

SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
,SUM(convert(bigint,vac.new_vaccinations)) OVER (Partition by dea.location order by dea.location, dea.date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
FROM CovidDeaths DEA JOIN CovidVaccinations VAC 
ON DEA.location = VAC.location
AND DEA.DATE = VAC.DATE
where dea.continent is not null
order by 2,3


--Use CTE

WITH PopvsVac (continent, location, date, population, new_vaccinations, RollingPeopleVaccinated)
as
(
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
,SUM(convert(bigint,vac.new_vaccinations)) OVER (Partition by dea.location order by dea.location, dea.date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
FROM CovidDeaths DEA JOIN CovidVaccinations VAC 
ON DEA.location = VAC.location
AND DEA.DATE = VAC.DATE
where dea.continent is not null
--order by 2,3
)
Select *, (RollingPeopleVaccinated/population)*100
from PopvsVac


-- Using Temp Table

DROP TABLE IF EXISTS #PercentPopulationVaccinated -- to modify
CREATE TABLE  #PercentPopulationVaccinated 
(continent nvarchar(255), location nvarchar(255), date datetime, population numeric, 
new_vaccinations numeric, RollingPeopleVaccinated  numeric)

INSERT INTO #PercentPopulationVaccinated
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
,SUM(convert(bigint,vac.new_vaccinations)) OVER (Partition by dea.location order by dea.location, dea.date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
FROM CovidDeaths DEA JOIN CovidVaccinations VAC 
ON DEA.location = VAC.location
AND DEA.DATE = VAC.DATE
where dea.continent is not null
--order by 2,3

Select *, (RollingPeopleVaccinated/population)*100
from #PercentPopulationVaccinated


--Creating View to store data for later visualizations

Create View PercentPopulationVaccinated as
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
,SUM(convert(bigint,vac.new_vaccinations)) OVER (Partition by dea.location order by dea.location, dea.date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
FROM CovidDeaths DEA JOIN CovidVaccinations VAC 
ON DEA.location = VAC.location
AND DEA.DATE = VAC.DATE
where dea.continent is not null
--order by 2,3

SELECT * FROM PercentPopulationVaccinated
