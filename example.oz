functor
import
  System
define
  declare
    class BaseQueue
      attr
        contents:nil
      meth enqueue(Item)
        raise notImplemented(self enqueue) end
      end
      %% Lazy list of indices of Y in Xs.
      fun {Indices Y Xs}
        for
          X in Xs
          I in 1;I+1
          yield:Yield
          {Browse "hello,\nworld!"}
        do
          if Y == X then {Yield I} end
        end
      end
    end
    Queue = {New BaseQueue init} %% throws
  end
end
