USE [Traffic_Crashes]
GO

/****** Object:  Table [dbo].[Crashes]    Script Date: 4/24/2025 3:29:48 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Crashes](
	[CRASH_RECORD_ID] [nvarchar](255) NOT NULL,
	[CRASH_DATE] [datetime] NULL,
	[POSTED_SPEED_LIMIT] [int] NULL,
	[TRAFFIC_CONTROL_DEVICE] [nvarchar](255) NULL,
	[DEVICE_CONDITION] [nvarchar](255) NULL,
	[WEATHER_CONDITION] [nvarchar](255) NULL,
	[LIGHTING_CONDITION] [nvarchar](255) NULL,
	[FIRST_CRASH_TYPE] [nvarchar](255) NULL,
	[TRAFFICWAY_TYPE] [nvarchar](255) NULL,
	[ALIGNMENT] [nvarchar](255) NULL,
	[ROADWAY_SURFACE_COND] [nvarchar](255) NULL,
	[ROAD_DEFECT] [nvarchar](255) NULL,
	[CRASH_TYPE] [nvarchar](255) NULL,
	[DAMAGE] [nvarchar](255) NULL,
	[PRIM_CONTRIBUTORY_CAUSE] [nvarchar](255) NULL,
	[SEC_CONTRIBUTORY_CAUSE] [nvarchar](255) NULL,
	[NUM_UNITS] [int] NULL,
	[MOST_SEVERE_INJURY] [nvarchar](255) NULL,
	[INJURIES_TOTAL] [int] NULL,
	[INJURIES_FATAL] [int] NULL,
	[CRASH_HOUR] [int] NULL,
	[CRASH_DAY_OF_WEEK] [int] NULL,
	[CRASH_MONTH] [int] NULL,
	[LATITUDE] [float] NULL,
	[LONGITUDE] [float] NULL,
	[CRASH_YEAR] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[CRASH_RECORD_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Crashes] ADD  CONSTRAINT [DF__Crashes__CRASH_D__3C69FB99]  DEFAULT (dateadd(minute,datediff(minute,(0),getdate()),(0))) FOR [CRASH_DATE]
GO

ALTER TABLE [dbo].[Crashes] ADD  CONSTRAINT [DF_Crashes_CRASH_HOUR]  DEFAULT (datepart(hour,getdate())) FOR [CRASH_HOUR]
GO

ALTER TABLE [dbo].[Crashes] ADD  CONSTRAINT [DF_Crashes_CRASH_DAY_OF_WEEK]  DEFAULT (datepart(weekday,getdate())) FOR [CRASH_DAY_OF_WEEK]
GO

ALTER TABLE [dbo].[Crashes] ADD  CONSTRAINT [DF_Crashes_CRASH_MONTH]  DEFAULT (datepart(month,getdate())) FOR [CRASH_MONTH]
GO

ALTER TABLE [dbo].[Crashes] ADD  CONSTRAINT [DF_Crashes_CRASH_YEAR]  DEFAULT (datepart(year,getdate())) FOR [CRASH_YEAR]
GO


