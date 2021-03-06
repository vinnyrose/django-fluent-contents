from django.core.cache import cache


class CachedModelMixin(object):
    """
    Mixin to add cache expiration to a model.
    """
    def save(self, *args, **kwargs):
        is_new = not self.pk or self._state.adding
        super(CachedModelMixin, self).save(*args, **kwargs)
        if not is_new:
            self.clear_cache()

    save.alters_data = True


    def delete(self, *args, **kwargs):
        super(CachedModelMixin, self).delete(*args, **kwargs)
        self.clear_cache()

    # Must restore these options, or risk removing with a template print statement.
    delete.alters_data = True


    def clear_cache(self):
        """
        Delete the cache keys associated with this model.
        """
        cache.delete_many(self.get_cache_keys())

    clear_cache.alters_data = True


    def get_cache_keys(self):
        """
        Get a list of all cache keys associated with this model.
        """
        raise NotImplementedError("Implement get_cache_keys() or clear_cache()")
