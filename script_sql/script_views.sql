create or replace view spotify_db.top_musicas_populares as
  select t.track_id, t.track_name, a.artist_name, p.track_popularity,
  p.data_popularidade, a.artist_genre
  from spotify_db.track as t
  inner join spotify_db.track_artist using (track_id)
  inner join spotify_db.artist as a using(artist_id)
  inner join spotify_db.track_popularity as p using (track_id)
  order by data_popularidade;

# ----------------------------------------------------------------------------------------------------------------------

create or replace view spotify_db.features_track as
  select track_name, track_liveness, track_speechness, track_valence, track_energy, track_acousticness, track_instrumentalness, track_dancebility
  from spotify_db.track;
# ----------------------------------------------------------------------------------------------------------------------

create or replace view spotify_db.musicas_por_genero
as select count(a.artist_id) as quant, a.artist_genre
from spotify_db.artist a
where a.artist_genre is not null
group by a.artist_genre order by quant desc;

# ----------------------------------------------------------------------------------------------------------------------
create or replace view spotify_db.features_artist as
  select a.artist_name, avg(track_liveness) as track_liveness, avg(track_speechness) as track_speechness,
        avg(track_valence) as track_valence, avg(track_energy) as track_energy, avg(track_acousticness) as track_acousticness, avg(track_instrumentalness) as track_instrumentalness,
         avg(track_dancebility) as track_dancebility
  from spotify_db.track t join spotify_db.track_artist ta on t.track_id = ta.track_id
        join  spotify_db.artist a on ta.artist_id = a.artist_id
  group by a.artist_name;

# ----------------------------------------------------------------------------------------------------------------------

create or replace view spotify_db.features_playlist as
  select a.playlist_name, avg(track_liveness) as track_liveness, avg(track_speechness) as track_speechness,
        avg(track_valence) as track_valence, avg(track_energy) as track_energy, avg(track_acousticness) as track_acousticness, avg(track_instrumentalness) as track_instrumentalness,
         avg(track_dancebility) as track_dancebility
  from spotify_db.track t join spotify_db.track_playlist ta on t.track_id = ta.track_id
        join  spotify_db.playlist a on ta.playlist_id = a.playlist_id
  group by a.playlist_name;

#-----------------------------------------------------------------------------------------------------------------------

create or replace view spotify_db.explicit_genre
as  select count(t.track_id) as quant, p.playlist_category
from spotify_db.track_artist a join spotify_db.track t on a.track_id = t.track_id
join spotify_db.track_playlist tp on t.track_id = tp.track_id
join spotify_db.playlist p on p.playlist_id = tp.playlist_id
where track_explicit = 't'
group by a.playlist_category order by quant desc;


create or replace view spotify_db.duration_track
as select track_id, track_duration from spotify_db.track;

# ----------------------------------------------------------------------------------------------------------------------
create or replace function spotify_db.top10_tracks(data date) returns table (Track varchar, Popularidade smallint) as $$
begin
  return query select t.track_name, tp.track_popularity
from spotify_db.track t join spotify_db.track_popularity tp on t.track_id = tp.track_id
where tp.data_popularidade = data
order by tp.track_popularity desc
limit 10;
end;
$$ language plpgsql;

# ----------------------------------------------------------------------------------------------------------------------
create or replace function spotify_db.top10_artist(data date) returns table (Artist varchar, Popularidade smallint) as $$
begin
  return query select a.artist_name, ap.artist_popularity
from spotify_db.artist a join spotify_db.artist_popularity ap on a.artist_id = ap.artist_id
where ap.data_popularidade = data
order by ap.artist_popularity desc
limit 10;
end;
$$ language plpgsql;

# ----------------------------------------------------------------------------------------------------------------------
create or replace function spotify_db.maior_decrescimo()
returns varchar as $$
declare pop spotify_db.min_max_dates%rowtype;
maior_dec int := 0;
id varchar := '';
begin
for pop in select * from spotify_db.min_max_dates
loop

if (pop.track_popularity - pop.min_pop) < maior_dec then
  maior_dec = (pop.track_popularity - pop.min_pop);
  id = pop.track_id;
end if;
end loop;
return id;
end;
$$ language plpgsql;

create or replace function spotify_db.maior_crescimento()
returns varchar as $$
declare pop spotify_db.min_max_dates%rowtype;
maior_cres int := 0;
id varchar := '';
begin
for pop in select * from spotify_db.min_max_dates
loop

if (pop.track_popularity - pop.min_pop) > maior_cres then
  maior_cres = (pop.track_popularity - pop.min_pop);
  id = pop.track_id;
end if;
end loop;
return id;
end;
$$ language plpgsql;


create or replace view spotify_db.max_date as
select a.track_id, track_popularity, a.data_popularidade from (select track_id, max(data_popularidade) as data_popularidade
from spotify_db.track_popularity group by track_id) a join spotify_db.track_popularity
t on t.track_id = a.track_id and t.data_popularidade = a.data_popularidade order by t.track_id

create or replace view as spotify_db.min_date
select a.track_id, track_popularity, a.data_popularidade from (select track_id, min(data_popularidade) as data_popularidade
from spotify_db.track_popularity group by track_id) a join spotify_db.track_popularity
t on t.track_id = a.track_id and t.data_popularidade = a.data_popularidade order by t.track_id

create or replace view spotify_db.min_max_dates as select max.track_id, data_popularidade, track_popularity, min_date, min_pop from spotify_db.max_date max join spotify_db.min_date min on max.track_id = min.track_id;


create or replace view spotify_db.quant_artist_category as
select p.playlist_category, count(a.artist_id) as quant
from spotify_db.track_artist a join spotify_db.track t on a.track_id = t.track_id
join spotify_db.track_playlist tp on t.track_id = tp.track_id
join spotify_db.playlist p on p.playlist_id = tp.playlist_id
group by p.playlist_category order by quant desc;